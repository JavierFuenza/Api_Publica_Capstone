"""
Water Quality Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseResponse(BaseModel):
    """Base schema for all responses."""
    model_config = ConfigDict(from_attributes=True)

# ============================
# Schemas for Water Quality Views
# ============================

class MarMensualSchema(BaseResponse):
    mes: str
    estacion: str
    temp_superficial_del_mar: Optional[float] = None
    nivel_medio_del_mar: Optional[float] = None

class GlaciaresAnualCuencaSchema(BaseResponse):
    anio: int
    cuenca: str
    num_glaciares_por_cuenca: Optional[int] = None
    superficie_de_glaciares_por_cuenca: Optional[float] = None
    volumen_de_hielo_glaciar_estimado_por_cuenca: Optional[float] = None
    volumen_de_agua_de_glaciares_estimada_por_cuenca: Optional[float] = None

# ============================
# Schemas for Water Quality Tables
# ============================

class ColiformesBiologicaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    value: int

class ColiformesAcuosaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    value: float

class MetalesSedimentariaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    parametros_poal: str
    value: float

class MetalesAcuosaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    parametros_poal: str
    value: float

class CaudalSchema(BaseResponse):
    mes: str
    aguas_corrientes: str
    estaciones_fluviometricas: str
    value: float

class LluviaSchema(BaseResponse):
    mes: str
    estaciones_meteorologicas_dmc: str
    value: float

class EvaporacionSchema(BaseResponse):
    mes: str
    estacion: str
    value: float

class EmbalseSchema(BaseResponse):
    mes: str
    embalse: str
    value: float

class NieveSchema(BaseResponse):
    dia: str
    estaciones_nivometricas: str
    value: int

class PozoSchema(BaseResponse):
    dia: str
    estaciones_pozo: str
    value: float
