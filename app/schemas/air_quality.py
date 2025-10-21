"""
Air Quality Pydantic schemas for request/response validation.

IMPORTANT: Update these schemas to match your actual database model.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class AirQualityBase(BaseModel):
    """Base schema with common fields."""

    measurement_date: datetime = Field(
        ...,
        description="Date and time of the measurement",
        examples=["2024-01-15T10:30:00"]
    )
    location: Optional[str] = Field(
        None,
        description="Location where measurement was taken",
        examples=["Downtown Station", "City Park"]
    )
    pm25: Optional[float] = Field(
        None,
        description="PM2.5 particulate matter (μg/m³)",
        examples=[12.5]
    )
    pm10: Optional[float] = Field(
        None,
        description="PM10 particulate matter (μg/m³)",
        examples=[25.3]
    )
    co: Optional[float] = Field(
        None,
        description="Carbon monoxide level (ppm)",
        examples=[0.5]
    )
    no2: Optional[float] = Field(
        None,
        description="Nitrogen dioxide level (ppb)",
        examples=[15.2]
    )
    so2: Optional[float] = Field(
        None,
        description="Sulfur dioxide level (ppb)",
        examples=[8.1]
    )
    o3: Optional[float] = Field(
        None,
        description="Ozone level (ppb)",
        examples=[42.5]
    )
    temperature: Optional[float] = Field(
        None,
        description="Temperature (°C)",
        examples=[22.5]
    )
    humidity: Optional[float] = Field(
        None,
        description="Relative humidity (%)",
        examples=[65.0]
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or observations",
        examples=["Clear skies"]
    )


class AirQualityResponse(AirQualityBase):
    """Schema for Air Quality response."""

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


class AirQualityListResponse(BaseModel):
    """Schema for list of air quality measurements."""

    data: list[AirQualityResponse] = Field(
        ...,
        description="List of air quality measurements"
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
                        "location": "Downtown Station",
                        "pm25": 12.5,
                        "pm10": 25.3,
                        "co": 0.5,
                        "no2": 15.2,
                        "so2": 8.1,
                        "o3": 42.5,
                        "temperature": 22.5,
                        "humidity": 65.0,
                        "notes": "Clear skies",
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
