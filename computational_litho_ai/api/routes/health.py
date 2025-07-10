from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.get("")
def read_root():
    """Simple health check endpoint."""
    return {"status": "ok"}

