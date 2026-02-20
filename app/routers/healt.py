from fastapi import APIRouter

router = APIRouter(prefix="/healt", tags=["healt"])

@router.get("/ping")
def ping():
    return {"status": "ok"}
