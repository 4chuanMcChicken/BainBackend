from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.db.session import get_db
from app.db.models import QueryHistory


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
    db: AsyncSession = Depends(get_db)
):
    """Get query history"""
    query = (
        select(QueryHistory)
        .order_by(QueryHistory.created_at.desc())
        .limit(limit)
    )
    
    result = await db.execute(query)
    return result.scalars().all() 