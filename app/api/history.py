from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel
from datetime import datetime
from loguru import logger

from app.db.session import get_db
from app.db.models import QueryHistory
from app.services.recaptcha import verify_recaptcha
import os


router = APIRouter()


class HistoryResponse(BaseModel):
    id: int
    source: str
    destination: str
    kilometers: float
    miles: float
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/history", response_model=List[HistoryResponse])
async def get_history(
    limit: int = Query(default=20, le=100),
    recaptcha_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Get query history
    
    This endpoint requires reCAPTCHA verification to prevent abuse.
    The client must provide a valid reCAPTCHA token.
    """
    logger.info(f"Fetching query history with limit {limit}")
    
    # Verify reCAPTCHA token
    await verify_recaptcha(recaptcha_token)

    # Query history after successful verification
    query = (
        select(QueryHistory)
        .order_by(QueryHistory.created_at.desc())
        .limit(limit)
    )
    
    result = await db.execute(query)
    history = result.scalars().all()
    
    logger.info(f"Retrieved {len(history)} history records")
    
    return history
