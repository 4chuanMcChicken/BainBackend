from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.db.session import get_db
from app.db.models import QueryHistory
from app.services.geocode import get_coordinates
from app.core.haversine import calculate_distance


router = APIRouter()


class DistanceRequest(BaseModel):
    source: str = Field(..., min_length=1, max_length=256)
    destination: str = Field(..., min_length=1, max_length=256)


class DistanceResponse(BaseModel):
    kilometers: float
    miles: float


@router.post("/distance", response_model=DistanceResponse)
async def calculate_distance_between(
    request: DistanceRequest,
    db: AsyncSession = Depends(get_db)
):
    """Calculate distance between two addresses"""
    logger.info(f"Calculating distance from '{request.source}' to '{request.destination}'")

    # Get coordinates for source address
    source_coords = await get_coordinates(request.source, "source")
    dest_coords   = await get_coordinates(request.destination, "destination")
    # Calculate distance
    kilometers, miles = calculate_distance(
        source_coords[0], source_coords[1],
        dest_coords[0], dest_coords[1]
    )

    # Store in database
    query_history = QueryHistory(
        source=request.source,
        destination=request.destination,
        kilometers=kilometers,
        miles=miles
    )
    db.add(query_history)
    await db.commit()
    logger.info(
        f"Stored distance calculation: {kilometers:.2f} km / {miles:.2f} miles "
        f"from '{request.source}' to '{request.destination}'"
    )


    return {"kilometers": kilometers, "miles": miles} 