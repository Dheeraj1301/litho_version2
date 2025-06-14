import os
import uuid
import shutil
import time
from io import BytesIO
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import torch
import torchvision.transforms as transforms
from ml.autoencoder.train_autoencoder import AutoEncoder

router = APIRouter()

# Load model
autoencoder_model = AutoEncoder()
autoencoder_model.load_state_dict(torch.load("ml/scripts/models/autoencoder.pt", map_location="cpu"))
autoencoder_model.eval()

# Transform for preprocessing
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

# Log directory for output
LOG_DIR = "ml/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def cleanup_old_files(directory: str, age_seconds: int = 600):
    now = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and (now - os.path.getmtime(file_path)) > age_seconds:
            os.remove(file_path)

@router.post("/infer")
async def infer_autoencoder(file: UploadFile = File(...)):
    try:
        cleanup_old_files(LOG_DIR)

        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("L")
        image_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            reconstructed = autoencoder_model(image_tensor)
            loss = torch.nn.functional.mse_loss(reconstructed, image_tensor)

        tensor_array = reconstructed.squeeze().numpy().tolist()

        file_id = str(uuid.uuid4())[:8]
        session_dir = os.path.join(LOG_DIR, f"session_{file_id}")
        os.makedirs(session_dir, exist_ok=True)

        # Save tensor as .txt
        tensor_txt_path = os.path.join(session_dir, "tensor.txt")
        with open(tensor_txt_path, "w") as f:
            for row in tensor_array:
                f.write(" ".join(f"{val:.6f}" for val in row) + "\n")

        # Save reconstructed image
        recon_img = transforms.ToPILImage()(reconstructed.squeeze(0))
        recon_img.save(os.path.join(session_dir, "reconstructed.png"))

        # Save original resized image
        orig_resized = transform(image).squeeze(0)
        transforms.ToPILImage()(orig_resized).save(os.path.join(session_dir, "original.png"))

        # Zip everything
        zip_base = os.path.join(LOG_DIR, f"autoencoder_{file_id}")
        shutil.make_archive(zip_base, 'zip', session_dir)

        return {
            "message": "Inference successful",
            "reconstruction_loss": round(loss.item(), 6),
            "download_zip": f"/autoencoder/download/{file_id}"
        }

    except Exception as e:
        return {"error": str(e)}

@router.get("/download/{file_id}")
def download_zip(file_id: str):
    zip_path = os.path.join(LOG_DIR, f"autoencoder_{file_id}.zip")
    if os.path.exists(zip_path):
        return FileResponse(zip_path, filename=f"autoencoder_{file_id}.zip", media_type="application/zip")
    return {"error": "File not found"}
