from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io
import torch
from torchvision import transforms
from PIL import Image
from ml.gated_cnn.gated_cnn_model import GatedCNN, predict_layout_class
from ml.autoencoder.train_autoencoder import AutoEncoder
from ml.yield_prediction.yield_predictor import YieldPredictor

router = APIRouter()

# Load models globally
gated_model = GatedCNN()
gated_model.load_state_dict(torch.load("ml/scripts/models/gated_cnn.pt", map_location="cpu"))
gated_model.eval()

autoencoder_model = AutoEncoder()
autoencoder_model.load_state_dict(torch.load("ml/scripts/models/autoencoder.pt", map_location="cpu"))
autoencoder_model.eval()

yield_model = YieldPredictor()
yield_model.load_model("ml/scripts/models/yield_predictor.joblib")
# Common image preprocessing
image_transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])


@router.post("/run")
async def run_csv_inference(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        if "target" in df.columns:
            X = df.drop(columns=["target"])
        else:
            X = df

        predictions = yield_model.predict(X)
        df["Predicted_Yield"] = predictions

        return {
            "message": "Inference completed",
            "rows_received": df.to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}


@router.post("/image/classify")
async def classify_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        input_tensor = image_transform(image).unsqueeze(0)

        predicted_class = predict_layout_class(gated_model, input_tensor)

        return {
            "message": "Classification done",
            "predicted_class": predicted_class
        }

    except Exception as e:
        return {"error": str(e)}


@router.post("/image/reconstruct")
async def reconstruct_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        input_tensor = image_transform(image).unsqueeze(0)

        with torch.no_grad():
            reconstructed = autoencoder_model(input_tensor)

        reconstructed_image = reconstructed.squeeze().numpy()
        reconstructed_list = reconstructed_image.tolist()

        return {
            "message": "Reconstruction completed",
            "reconstructed_tensor": reconstructed_list
        }

    except Exception as e:
        return {"error": str(e)}
