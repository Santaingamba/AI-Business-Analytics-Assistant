from fastapi import APIRouter
from app.schemas.common import StandardResponse

router = APIRouter()

@router.get("", response_model=StandardResponse)
def check_health():
    return StandardResponse(
        success=True,
        message="Backend is healthy",
        data={"status": "ok"}
    )
