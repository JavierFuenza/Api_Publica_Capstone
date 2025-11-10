"""
Air Quality API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, get_current_user_optional, FirebaseUser
from app.models.air_quality import *
from app.schemas.air_quality import *
from typing import Optional

# Create sub-routers to organize endpoints
climaticos_router = APIRouter(
    prefix="/climaticos",
    tags=["Air Quality - Climate"],
    responses={404: {"description": "Not found"}}
)

mp25_router = APIRouter(
    prefix="/mp25",
    tags=["Air Quality - PM2.5"],
    responses={404: {"description": "Not found"}}
)

mp10_router = APIRouter(
    prefix="/mp10",
    tags=["Air Quality - PM10"],
    responses={404: {"description": "Not found"}}
)

o3_router = APIRouter(
    prefix="/o3",
    tags=["Air Quality - Ozone (O3)"],
    responses={404: {"description": "Not found"}}
)

so2_router = APIRouter(
    prefix="/so2",
    tags=["Air Quality - Sulfur Dioxide (SO2)"],
    responses={404: {"description": "Not found"}}
)

no2_router = APIRouter(
    prefix="/no2",
    tags=["Air Quality - Nitrogen Dioxide (NO2)"],
    responses={404: {"description": "Not found"}}
)

co_router = APIRouter(
    prefix="/co",
    tags=["Air Quality - Carbon Monoxide (CO)"],
    responses={404: {"description": "Not found"}}
)

no_router = APIRouter(
    prefix="/no",
    tags=["Air Quality - Nitrogen Oxide (NO)"],
    responses={404: {"description": "Not found"}}
)

nox_router = APIRouter(
    prefix="/nox",
    tags=["Air Quality - Nitrogen Oxides (NOx)"],
    responses={404: {"description": "Not found"}}
)

eventos_router = APIRouter(
    prefix="/eventos",
    tags=["Air Quality - Climate Events"],
    responses={404: {"description": "Not found"}}
)

# Main router to include in main.py
router = APIRouter()

# ============================
# Climate endpoints
# ============================

@climaticos_router.get("/temperatura", response_model=List[TemperaturaSchema])
async def get_temperatura(
    db: Session = Depends(get_db),
    current_user: Optional[FirebaseUser] = Depends(get_current_user_optional)
):
    """Get all temperature data by station and month."""
    data = db.query(VTemperatura).all()
    return data

@climaticos_router.get("/humedad-radiacion-uv", response_model=List[HumedadRadiacionUVSchema])
async def get_humedad_radiacion_uv(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Get relative humidity, global radiation and UVB radiation data."""
    data = db.query(VHumedadRadiacionUV).all()
    return data

# ============================
# PM2.5 endpoints
# ============================

@mp25_router.get("/anual", response_model=List[Mp25AnualSchema])
async def get_mp25_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual PM2.5 data - statistics by station."""
    data = db.query(VMp25Anual).all()
    return data

@mp25_router.get("/mensual", response_model=List[Mp25MensualSchema])
async def get_mp25_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly PM2.5 data - average by station."""
    data = db.query(VMp25Mensual).all()
    return data

# ============================
# PM10 endpoints
# ============================

@mp10_router.get("/anual", response_model=List[Mp10AnualSchema])
async def get_mp10_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual PM10 data - statistics by station."""
    data = db.query(VMp10Anual).all()
    return data

@mp10_router.get("/mensual", response_model=List[Mp10MensualSchema])
async def get_mp10_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly PM10 data - average by station."""
    data = db.query(VMp10Mensual).all()
    return data

# ============================
# O3 endpoints
# ============================

@o3_router.get("/anual", response_model=List[O3AnualSchema])
async def get_o3_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual tropospheric ozone data - statistics by station."""
    data = db.query(VO3Anual).all()
    return data

@o3_router.get("/mensual", response_model=List[O3MensualSchema])
async def get_o3_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly tropospheric ozone data - average by station."""
    data = db.query(VO3Mensual).all()
    return data

# ============================
# SO2 endpoints
# ============================

@so2_router.get("/anual", response_model=List[So2AnualSchema])
async def get_so2_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual SO2 data - statistics by monitoring station."""
    data = db.query(VSo2Anual).all()
    return data

@so2_router.get("/mensual", response_model=List[So2MensualSchema])
async def get_so2_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly SO2 data - average by monitoring station."""
    data = db.query(VSo2Mensual).all()
    return data

# ============================
# NO2 endpoints
# ============================

@no2_router.get("/anual", response_model=List[No2AnualSchema])
async def get_no2_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual NO2 data - statistics by monitoring station."""
    data = db.query(VNo2Anual).all()
    return data

@no2_router.get("/mensual", response_model=List[No2MensualSchema])
async def get_no2_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly NO2 data - average by monitoring station."""
    data = db.query(VNo2Mensual).all()
    return data

# ============================
# CO endpoints
# ============================

@co_router.get("/anual", response_model=List[CoAnualSchema])
async def get_co_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual CO data - statistics by monitoring station."""
    data = db.query(VCoAnual).all()
    return data

@co_router.get("/mensual", response_model=List[CoMensualSchema])
async def get_co_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly CO data - average by monitoring station."""
    data = db.query(VCoMensual).all()
    return data

# ============================
# NO endpoints
# ============================

@no_router.get("/anual", response_model=List[NoAnualSchema])
async def get_no_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual NO data - statistics by monitoring station."""
    data = db.query(VNoAnual).all()
    return data

@no_router.get("/mensual", response_model=List[NoMensualSchema])
async def get_no_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly NO data - average by monitoring station."""
    data = db.query(VNoMensual).all()
    return data

# ============================
# NOx endpoints
# ============================

@nox_router.get("/anual", response_model=List[NoxAnualSchema])
async def get_nox_anual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Annual NOx data - statistics by monitoring station."""
    data = db.query(VNoxAnual).all()
    return data

@nox_router.get("/mensual", response_model=List[NoxMensualSchema])
async def get_nox_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly NOx data - average by monitoring station."""
    data = db.query(VNoxMensual).all()
    return data

# ============================
# Climate events endpoints
# ============================

@eventos_router.get("/olas-calor", response_model=List[OlasCalorSchema])
async def get_olas_calor(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Number of heat wave events by region and year."""
    data = db.query(VNumEventosDeOlasDeCalor).all()
    return data

# Include sub-routers in main router
router.include_router(climaticos_router)
router.include_router(mp25_router)
router.include_router(mp10_router)
router.include_router(o3_router)
router.include_router(so2_router)
router.include_router(no2_router)
router.include_router(co_router)
router.include_router(no_router)
router.include_router(nox_router)
router.include_router(eventos_router)
