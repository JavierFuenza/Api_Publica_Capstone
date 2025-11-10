"""
Air Quality Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseResponse(BaseModel):
    """Base schema for all responses."""
    model_config = ConfigDict(from_attributes=True)

# ============================
# Schemas for Air Quality Views
# ============================

class TemperaturaSchema(BaseResponse):
    mes: str
    estacion: str
    temp_max_absoluta: Optional[float] = None
    temp_min_absoluta: Optional[float] = None
    temp_max_med: Optional[float] = None
    temp_min_med: Optional[float] = None
    temp_med: Optional[float] = None

class HumedadRadiacionUVSchema(BaseResponse):
    mes: str
    estacion: str
    humedad_rel_med_mens: Optional[float] = None
    rad_global_med: Optional[int] = None
    uvb_prom: Optional[float] = None

class Mp25AnualSchema(BaseResponse):
    anio: int
    estacion: str
    mp25_max_hor_anual: Optional[float] = None
    mp25_min_hor_anual: Optional[float] = None
    mp25_perc50: Optional[float] = None
    mp25_perc90: Optional[float] = None
    mp25_perc95: Optional[float] = None
    mp25_perc98: Optional[int] = None

class Mp25MensualSchema(BaseResponse):
    mes: str
    estacion: str
    mp25_med_mens: Optional[float] = None

class Mp10AnualSchema(BaseResponse):
    anio: int
    estacion: str
    mp10_max_hor_anual: Optional[float] = None
    mp10_min_hor_anual: Optional[float] = None
    mp10_perc50: Optional[float] = None
    mp10_perc90: Optional[float] = None
    mp10_perc95: Optional[float] = None
    mp10_perc98: Optional[int] = None

class Mp10MensualSchema(BaseResponse):
    mes: str
    estacion: str
    mp10_med_mens: Optional[int] = None

class O3AnualSchema(BaseResponse):
    anio: int
    estacion: str
    o3_max_hor_anual: Optional[float] = None
    o3_min_hor_anual: Optional[float] = None
    o3_perc50: Optional[float] = None
    o3_perc90: Optional[float] = None
    o3_perc95: Optional[float] = None
    o3_perc98: Optional[float] = None
    o3_perc99: Optional[float] = None

class O3MensualSchema(BaseResponse):
    mes: str
    estacion: str
    o3_med_mens: Optional[float] = None

class So2AnualSchema(BaseResponse):
    anio: int
    estacion: str
    so2_max_hor_anual: Optional[float] = None
    so2_min_anual: Optional[float] = None
    so2_perc50: Optional[float] = None
    so2_perc90: Optional[float] = None
    so2_perc95: Optional[float] = None
    so2_perc98: Optional[float] = None
    so2_perc99: Optional[float] = None

class So2MensualSchema(BaseResponse):
    mes: str
    estacion: str
    so2_med_mens: Optional[float] = None

class No2AnualSchema(BaseResponse):
    anio: int
    estacion: str
    no2_max_hor_anual: Optional[float] = None
    no2_min_hor_anual: Optional[float] = None
    no2_perc50: Optional[float] = None
    no2_perc90: Optional[float] = None
    no2_perc95: Optional[float] = None
    no2_perc98: Optional[float] = None
    no2_perc99: Optional[float] = None

class No2MensualSchema(BaseResponse):
    mes: str
    estacion: str
    no2_med_mens: Optional[float] = None

class CoAnualSchema(BaseResponse):
    anio: int
    estacion: str
    co_max_hor_anual: Optional[float] = None
    co_min_hor_anual: Optional[float] = None
    co_perc50: Optional[float] = None
    co_perc90: Optional[float] = None
    co_perc95: Optional[float] = None
    co_perc98: Optional[float] = None
    co_perc99: Optional[float] = None

class CoMensualSchema(BaseResponse):
    mes: str
    estacion: str
    co_med_mens: Optional[float] = None

class NoAnualSchema(BaseResponse):
    anio: int
    estacion: str
    no_max_hor_anual: Optional[float] = None
    no_min_hor_anual: Optional[float] = None
    no_perc50: Optional[float] = None
    no_perc90: Optional[float] = None
    no_perc95: Optional[float] = None
    no_perc98: Optional[float] = None
    no_perc99: Optional[float] = None

class NoMensualSchema(BaseResponse):
    mes: str
    estacion: str
    no_med_mens: Optional[float] = None

class NoxAnualSchema(BaseResponse):
    anio: int
    estacion: str
    nox_max_hor_anual: Optional[float] = None
    nox_min_hor_anual: Optional[float] = None
    nox_perc50: Optional[float] = None
    nox_perc90: Optional[float] = None
    nox_perc95: Optional[float] = None
    nox_perc98: Optional[float] = None
    nox_perc99: Optional[float] = None

class NoxMensualSchema(BaseResponse):
    mes: str
    estacion: str
    nox_med_mens: Optional[float] = None

class OlasCalorSchema(BaseResponse):
    mes: str
    estacion: str
    num_eventos_de_olas_de_calor: Optional[int] = None
