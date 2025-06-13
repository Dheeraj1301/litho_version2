from fastapi import APIRouter

router = APIRouter()

@router.get("/Ping")
def health_check():
    return {"status": "ok"}
