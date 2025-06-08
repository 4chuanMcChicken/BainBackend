from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.db.session import get_db
from app.db.models import QueryHistory
from app.services.geocode import get_coordinates
from app.services.address_cleaner import clean_addresses
from app.core.haversine import calculate_distance


router = APIRouter()


class DistanceRequest(BaseModel):
    source: str = Field(..., min_length=1, max_length=256)
    destination: str = Field(..., min_length=1, max_length=256)


class DistanceResponse(BaseModel):
    kilometers: float
    miles: float
    source_address: str  # 清理后的源地址
    destination_address: str  # 清理后的目标地址
    source_corrected: bool
    destination_corrected: bool


@router.post("/distance", response_model=DistanceResponse)
async def calculate_distance_between(
    request: DistanceRequest,
    db: AsyncSession = Depends(get_db)
):
    """Calculate distance between two addresses"""
    logger.info(f"Calculating distance from '{request.source}' to '{request.destination}'")

    # Clean and correct addresses
    cleaned = await clean_addresses(request.source, request.destination)
    source = cleaned["source"]
    destination = cleaned["destination"]
    
    logger.info(
        f"Address cleaning results - "
        f"Source: '{request.source}' -> '{source}' (corrected: {cleaned['sourceCorrected']}), "
        f"Destination: '{request.destination}' -> '{destination}' (corrected: {cleaned['destinationCorrected']})"
    )

    # Get coordinates for addresses
    source_coords = await get_coordinates(source, "source")
    dest_coords = await get_coordinates(destination, "destination")

    # Calculate distance
    kilometers, miles = calculate_distance(
        source_coords[0], source_coords[1],
        dest_coords[0], dest_coords[1]
    )

    # Store in database
    query_history = QueryHistory(
        source=source,
        destination=destination,
        kilometers=kilometers,
        miles=miles
    )
    db.add(query_history)
    await db.commit()

    logger.info(
        f"Stored distance calculation: {kilometers:.2f} km / {miles:.2f} miles "
        f"from '{source}' to '{destination}'"
    )

    return {
        "kilometers": kilometers,
        "miles": miles,
        "source_address": source,
        "destination_address": destination,
        "source_corrected": cleaned["sourceCorrected"],
        "destination_corrected": cleaned["destinationCorrected"]
    } 