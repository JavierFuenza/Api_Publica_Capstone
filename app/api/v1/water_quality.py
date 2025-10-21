"""
Water Quality API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, FirebaseUser
from app.models.water_quality import WaterQuality
from app.schemas.water_quality import WaterQualityResponse, WaterQualityListResponse

router = APIRouter()


@router.get(
    "/",
    response_model=WaterQualityListResponse,
    summary="Get water quality measurements",
    description="""
    Retrieve a list of water quality measurements with optional filtering.

    **Authentication required**: Include Firebase ID token in Authorization header.

    **Filters:**
    - `date_from`: Get measurements from this date onwards
    - `date_to`: Get measurements up to this date
    - `location`: Filter by location name (partial match)
    - `source`: Filter by water source type
    - `limit`: Maximum number of records to return (default: 100, max: 1000)
    - `offset`: Number of records to skip for pagination (default: 0)

    **Example Response:**
    ```json
    {
        "data": [
            {
                "id": 1,
                "measurement_date": "2024-01-15T10:30:00",
                "location": "River Station A",
                "source": "River",
                "ph": 7.2,
                "dissolved_oxygen": 8.5,
                ...
            }
        ],
        "total": 150,
        "limit": 100,
        "offset": 0
    }
    ```
    """
)
async def get_water_quality_list(
    date_from: Optional[datetime] = Query(
        None,
        description="Filter measurements from this date (ISO format)"
    ),
    date_to: Optional[datetime] = Query(
        None,
        description="Filter measurements up to this date (ISO format)"
    ),
    location: Optional[str] = Query(
        None,
        description="Filter by location (partial match)"
    ),
    source: Optional[str] = Query(
        None,
        description="Filter by water source type"
    ),
    limit: int = Query(
        100,
        ge=1,
        le=1000,
        description="Maximum number of records to return"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of records to skip"
    ),
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Get list of water quality measurements with optional filters."""

    # Build query
    query = db.query(WaterQuality)

    # Apply filters
    if date_from:
        query = query.filter(WaterQuality.measurement_date >= date_from)

    if date_to:
        query = query.filter(WaterQuality.measurement_date <= date_to)

    if location:
        query = query.filter(WaterQuality.location.ilike(f"%{location}%"))

    if source:
        query = query.filter(WaterQuality.source.ilike(f"%{source}%"))

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    measurements = (
        query
        .order_by(WaterQuality.measurement_date.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return WaterQualityListResponse(
        data=measurements,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get(
    "/{measurement_id}",
    response_model=WaterQualityResponse,
    summary="Get specific water quality measurement",
    description="""
    Retrieve a specific water quality measurement by ID.

    **Authentication required**: Include Firebase ID token in Authorization header.

    **Example Response:**
    ```json
    {
        "id": 1,
        "measurement_date": "2024-01-15T10:30:00",
        "location": "River Station A",
        "source": "River",
        "ph": 7.2,
        "dissolved_oxygen": 8.5,
        ...
    }
    ```
    """
)
async def get_water_quality_by_id(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Get a specific water quality measurement by ID."""

    measurement = db.query(WaterQuality).filter(WaterQuality.id == measurement_id).first()

    if not measurement:
        raise HTTPException(
            status_code=404,
            detail=f"Water quality measurement with ID {measurement_id} not found"
        )

    return measurement
