"""
Water Quality API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, FirebaseUser
from app.models.water_quality import *
from app.schemas.water_quality import *

# Create sub-routers to organize endpoints by category
vistas_router = APIRouter(
    prefix="/vistas",
    tags=["Water Quality - General Views"],
    responses={404: {"description": "Not found"}}
)

contaminantes_router = APIRouter(
    prefix="/contaminantes",
    tags=["Water Quality - Contaminants"],
    responses={404: {"description": "Not found"}}
)

hidrologia_router = APIRouter(
    prefix="/hidrologia",
    tags=["Water Quality - Hydrology"],
    responses={404: {"description": "Not found"}}
)

meteorologicos_router = APIRouter(
    prefix="/meteorologicos",
    tags=["Water Quality - Meteorological"],
    responses={404: {"description": "Not found"}}
)

almacenamiento_router = APIRouter(
    prefix="/almacenamiento",
    tags=["Water Quality - Storage"],
    responses={404: {"description": "Not found"}}
)

# Main router to include in main.py
router = APIRouter()

# ============================
# Views (return full table)
# ============================

@vistas_router.get("/mar-mensual", response_model=List[MarMensualSchema])
async def get_mar_mensual(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Get all monthly sea data - Complete view."""
    data = db.query(VMarMensual).all()
    return data

@vistas_router.get("/glaciares-anual-cuenca", response_model=List[GlaciaresAnualCuencaSchema])
async def get_glaciares_anual_cuenca(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Get all annual glacier data by basin - Complete view."""
    data = db.query(VGlaciaresAnualCuenca).all()
    return data

# ============================
# Tables (specific fields only)
# ============================

@contaminantes_router.get("/coliformes-biologica", response_model=List[ColiformesBiologicaSchema])
async def get_coliformes_biologica(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Fecal coliforms in biological matrix by POAL station and date."""
    data = db.query(
        ColiformesFecalesEnMatrizBiologica.dia,
        ColiformesFecalesEnMatrizBiologica.estaciones_poal,
        ColiformesFecalesEnMatrizBiologica.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "value": row[2]} for row in data]

@contaminantes_router.get("/coliformes-acuosa", response_model=List[ColiformesAcuosaSchema])
async def get_coliformes_acuosa(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Fecal coliforms in aqueous matrix by POAL station and date."""
    data = db.query(
        ColiformesFecalesEnMatrizAcuosa.dia,
        ColiformesFecalesEnMatrizAcuosa.estaciones_poal,
        ColiformesFecalesEnMatrizAcuosa.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "value": row[2]} for row in data]

@contaminantes_router.get("/metales-sedimentaria", response_model=List[MetalesSedimentariaSchema])
async def get_metales_sedimentaria(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Total metals in sedimentary matrix by metal type and station."""
    data = db.query(
        MetalesTotalesEnLaMatrizSedimentaria.dia,
        MetalesTotalesEnLaMatrizSedimentaria.estaciones_poal,
        MetalesTotalesEnLaMatrizSedimentaria.parametros_poal,
        MetalesTotalesEnLaMatrizSedimentaria.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "parametros_poal": row[2], "value": row[3]} for row in data]

@contaminantes_router.get("/metales-acuosa", response_model=List[MetalesAcuosaSchema])
async def get_metales_acuosa(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Dissolved metals in aqueous matrix by metal type and station."""
    data = db.query(
        MetalesDisueltosEnLaMatrizAcuosa.dia,
        MetalesDisueltosEnLaMatrizAcuosa.estaciones_poal,
        MetalesDisueltosEnLaMatrizAcuosa.parametros_poal,
        MetalesDisueltosEnLaMatrizAcuosa.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "parametros_poal": row[2], "value": row[3]} for row in data]

@hidrologia_router.get("/caudal", response_model=List[CaudalSchema])
async def get_caudal(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly average flow of running water by fluviometric station."""
    data = db.query(
        CaudalMedioDeAguasCorrientes.mes,
        CaudalMedioDeAguasCorrientes.aguas_corrientes,
        CaudalMedioDeAguasCorrientes.estaciones_fluviometricas,
        CaudalMedioDeAguasCorrientes.value
    ).all()
    return [{"mes": row[0], "aguas_corrientes": row[1], "estaciones_fluviometricas": row[2], "value": row[3]} for row in data]

@hidrologia_router.get("/pozos", response_model=List[PozoSchema])
async def get_pozos(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Static level of groundwater by well station."""
    data = db.query(
        NivelEstaticoDeAguasSubterraneas.dia,
        NivelEstaticoDeAguasSubterraneas.estaciones_pozo,
        NivelEstaticoDeAguasSubterraneas.value
    ).all()
    return [{"dia": row[0], "estaciones_pozo": row[1], "value": row[2]} for row in data]

@meteorologicos_router.get("/lluvia", response_model=List[LluviaSchema])
async def get_lluvia(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly precipitation by DMC meteorological station."""
    data = db.query(
        CantidadDeAguaCaida.mes,
        CantidadDeAguaCaida.estaciones_meteorologicas_dmc,
        CantidadDeAguaCaida.value
    ).all()
    return [{"mes": row[0], "estaciones_meteorologicas_dmc": row[1], "value": row[2]} for row in data]

@meteorologicos_router.get("/evaporacion", response_model=List[EvaporacionSchema])
async def get_evaporacion(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Real monthly evaporation by meteorological station."""
    data = db.query(
        EvaporacionRealPorEstacion.mes,
        EvaporacionRealPorEstacion.estacion,
        EvaporacionRealPorEstacion.value
    ).all()
    return [{"mes": row[0], "estacion": row[1], "value": row[2]} for row in data]

@meteorologicos_router.get("/nieve", response_model=List[NieveSchema])
async def get_nieve(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Snow height equivalent in water by nivometric station."""
    data = db.query(
        AlturaNieveEquivalenteEnAgua.dia,
        AlturaNieveEquivalenteEnAgua.estaciones_nivometricas,
        AlturaNieveEquivalenteEnAgua.value
    ).all()
    return [{"dia": row[0], "estaciones_nivometricas": row[1], "value": row[2]} for row in data]

@almacenamiento_router.get("/embalses", response_model=List[EmbalseSchema])
async def get_embalses(
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """Monthly volume stored by reservoir throughout Chile."""
    data = db.query(
        VolumenDelEmbalsePorEmbalse.mes,
        VolumenDelEmbalsePorEmbalse.embalse,
        VolumenDelEmbalsePorEmbalse.value
    ).all()
    return [{"mes": row[0], "embalse": row[1], "value": row[2]} for row in data]

# Include sub-routers in main router
router.include_router(vistas_router)
router.include_router(contaminantes_router)
router.include_router(hidrologia_router)
router.include_router(meteorologicos_router)
router.include_router(almacenamiento_router)
