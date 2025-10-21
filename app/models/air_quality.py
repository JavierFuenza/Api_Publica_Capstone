"""
Air Quality database models.

IMPORTANT: These are placeholder models. Update them to match your actual database schema.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime

from app.core.database import Base


class AirQuality(Base):
    """
    Air Quality measurement model.

    TODO: Update this model to match your actual database table structure.
    Common fields for air quality might include:
    - PM2.5, PM10 (particulate matter)
    - CO, CO2 (carbon monoxide/dioxide)
    - NO2, SO2 (nitrogen/sulfur dioxide)
    - O3 (ozone)
    - Temperature, humidity
    - Location/coordinates
    - Timestamp
    """

    __tablename__ = "air_quality"

    # Example fields - customize based on your actual schema
    id = Column(Integer, primary_key=True, index=True)
    measurement_date = Column(DateTime, nullable=False, index=True)
    location = Column(String(255), nullable=True)

    # Air quality metrics (example - adjust to your schema)
    pm25 = Column(Float, nullable=True, comment="PM2.5 particulate matter")
    pm10 = Column(Float, nullable=True, comment="PM10 particulate matter")
    co = Column(Float, nullable=True, comment="Carbon monoxide")
    no2 = Column(Float, nullable=True, comment="Nitrogen dioxide")
    so2 = Column(Float, nullable=True, comment="Sulfur dioxide")
    o3 = Column(Float, nullable=True, comment="Ozone")

    # Environmental conditions
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    # Metadata
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<AirQuality(id={self.id}, location={self.location}, date={self.measurement_date})>"
