from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"} 