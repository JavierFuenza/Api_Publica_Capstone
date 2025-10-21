"""
Water Quality Pydantic schemas for request/response validation.

IMPORTANT: Update these schemas to match your actual database model.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class WaterQualityBase(BaseModel):
    """Base schema with common fields."""

    measurement_date: datetime = Field(
        ...,
        description="Date and time of the measurement",
        examples=["2024-01-15T10:30:00"]
    )
    location: Optional[str] = Field(
        None,
        description="Location where measurement was taken",
        examples=["River Station A", "Lake Monitor Point"]
    )
    source: Optional[str] = Field(
        None,
        description="Water source type",
        examples=["River", "Lake", "Groundwater"]
    )
    ph: Optional[float] = Field(
        None,
        description="pH level (0-14 scale)",
        examples=[7.2]
    )
    dissolved_oxygen: Optional[float] = Field(
        None,
        description="Dissolved oxygen (mg/L)",
        examples=[8.5]
    )
    turbidity: Optional[float] = Field(
        None,
        description="Turbidity (NTU)",
        examples=[2.1]
    )
    temperature: Optional[float] = Field(
        None,
        description="Water temperature (°C)",
        examples=[18.5]
    )
    conductivity: Optional[float] = Field(
        None,
        description="Electrical conductivity (μS/cm)",
        examples=[450.0]
    )
    nitrates: Optional[float] = Field(
        None,
        description="Nitrate levels (mg/L)",
        examples=[1.2]
    )
    phosphates: Optional[float] = Field(
        None,
        description="Phosphate levels (mg/L)",
        examples=[0.05]
    )
    chlorine: Optional[float] = Field(
        None,
        description="Chlorine levels (mg/L)",
        examples=[0.3]
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or observations",
        examples=["Normal conditions"]
    )


class WaterQualityResponse(WaterQualityBase):
    """Schema for Water Quality response."""

    id: int = Field(
        ...,
        description="Unique identifier for the measurement"
    )
    created_at: datetime = Field(
        ...,
        description="Record creation timestamp"
    )
    updated_at: datetime = Field(
        ...,
        description="Record last update timestamp"
    )

    model_config = ConfigDict(from_attributes=True)


class WaterQualityListResponse(BaseModel):
    """Schema for list of water quality measurements."""

    data: list[WaterQualityResponse] = Field(
        ...,
        description="List of water quality measurements"
    )
    total: int = Field(
        ...,
        description="Total number of records matching the query"
    )
    limit: int = Field(
        ...,
        description="Maximum number of records returned"
    )
    offset: int = Field(
        0,
        description="Number of records skipped"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": [
                    {
                        "id": 1,
                        "measurement_date": "2024-01-15T10:30:00",
                        "location": "River Station A",
                        "source": "River",
                        "ph": 7.2,
                        "dissolved_oxygen": 8.5,
                        "turbidity": 2.1,
                        "temperature": 18.5,
                        "conductivity": 450.0,
                        "nitrates": 1.2,
                        "phosphates": 0.05,
                        "chlorine": 0.3,
                        "notes": "Normal conditions",
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00"
                    }
                ],
                "total": 1,
                "limit": 100,
                "offset": 0
            }
        }
    )
