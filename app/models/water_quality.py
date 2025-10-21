"""
Water Quality database models.

IMPORTANT: These are placeholder models. Update them to match your actual database schema.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime

from app.core.database import Base


class WaterQuality(Base):
    """
    Water Quality measurement model.

    TODO: Update this model to match your actual database table structure.
    Common fields for water quality might include:
    - pH level
    - Dissolved oxygen
    - Turbidity
    - Temperature
    - Conductivity
    - Contaminants (nitrates, phosphates, etc.)
    - Location/source
    - Timestamp
    """

    __tablename__ = "water_quality"

    # Example fields - customize based on your actual schema
    id = Column(Integer, primary_key=True, index=True)
    measurement_date = Column(DateTime, nullable=False, index=True)
    location = Column(String(255), nullable=True)
    source = Column(String(100), nullable=True, comment="Water source type")

    # Water quality metrics (example - adjust to your schema)
    ph = Column(Float, nullable=True, comment="pH level")
    dissolved_oxygen = Column(Float, nullable=True, comment="Dissolved oxygen (mg/L)")
    turbidity = Column(Float, nullable=True, comment="Turbidity (NTU)")
    temperature = Column(Float, nullable=True, comment="Water temperature")
    conductivity = Column(Float, nullable=True, comment="Electrical conductivity")

    # Chemical parameters
    nitrates = Column(Float, nullable=True, comment="Nitrate levels (mg/L)")
    phosphates = Column(Float, nullable=True, comment="Phosphate levels (mg/L)")
    chlorine = Column(Float, nullable=True, comment="Chlorine levels (mg/L)")

    # Metadata
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<WaterQuality(id={self.id}, location={self.location}, date={self.measurement_date})>"
