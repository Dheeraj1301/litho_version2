from fastapi import APIRouter, Query
from api.services.inference_service import run_inference

router = APIRouter()

@router.get("/")
def infer(mask_id: str = Query(...), model: str = Query(default="gated_cnn")):
    result = run_inference(mask_id=mask_id, model=model)
    return {"inference_result": result}
