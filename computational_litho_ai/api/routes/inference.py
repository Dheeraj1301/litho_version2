from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter()

@router.post("/run")
async def run_inference(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        print("✅ CSV uploaded:")
        print(df.head())  # Log for debugging

        # Dummy inference logic
        result = {"message": "Inference completed", "rows_received": len(df)}

        return result

    except Exception as e:
        return {"error": str(e)}
