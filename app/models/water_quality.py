"""
Water Quality database models - matching actual database schema.
"""

from sqlalchemy import Column, String, Float, BigInteger
from app.core.database import Base

# ============================
# Vista de Mar
# ============================
class VMarMensual(Base):
    __tablename__ = "v_mar_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(String, primary_key=True)
    estacion = Column(String, primary_key=True)

    temp_superficial_del_mar = Column(Float)
    nivel_medio_del_mar = Column(Float)

# ============================
# Vista de Glaciares
# ============================
class VGlaciaresAnualCuenca(Base):
    __tablename__ = "v_glaciares_anual_cuenca"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    cuenca = Column(String, primary_key=True)

    num_glaciares_por_cuenca = Column(BigInteger)
    superficie_de_glaciares_por_cuenca = Column(Float)
    volumen_de_hielo_glaciar_estimado_por_cuenca = Column(Float)
    volumen_de_agua_de_glaciares_estimada_por_cuenca = Column(Float)

# ============================
# Coliformes (POAL) - diaria
# ============================
class ColiformesFecalesEnMatrizBiologica(Base):
    __tablename__ = "coliformes_fecales_en_matriz_biologica"
    __table_args__ = {"schema": "public"}

    dti_cl_dia = Column(BigInteger, primary_key=True)
    dti_cl_t013est_poal = Column(String, primary_key=True)

    dia = Column(String)
    estaciones_poal = Column(String)
    value = Column(BigInteger)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)


class ColiformesFecalesEnMatrizAcuosa(Base):
    __tablename__ = "coliformes_fecales_en_matriz_acuosa"
    __table_args__ = {"schema": "public"}

    dti_cl_dia = Column(BigInteger, primary_key=True)
    dti_cl_t013est_poal = Column(String, primary_key=True)

    dia = Column(String)
    estaciones_poal = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)

# =========================================
# Metales (POAL) - diaria, con parámetro
# =========================================
class MetalesTotalesEnLaMatrizSedimentaria(Base):
    __tablename__ = "metales_totales_en_la_matriz_sedimentaria"
    __table_args__ = {"schema": "public"}

    dti_cl_dia = Column(BigInteger, primary_key=True)
    dti_cl_t013est_poal = Column(String, primary_key=True)
    dti_cl_t014param_poal = Column(String, primary_key=True)

    dia = Column(String)
    estaciones_poal = Column(String)
    parametros_poal = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)


class MetalesDisueltosEnLaMatrizAcuosa(Base):
    __tablename__ = "metales_disueltos_en_la_matriz_acuosa"
    __table_args__ = {"schema": "public"}

    dti_cl_dia = Column(BigInteger, primary_key=True)
    dti_cl_t013est_poal = Column(String, primary_key=True)
    dti_cl_t014param_poal = Column(String, primary_key=True)

    dia = Column(String)
    estaciones_poal = Column(String)
    parametros_poal = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)

# ============================
# Caudal (Fluviometría) - mensual
# ============================
class CaudalMedioDeAguasCorrientes(Base):
    __tablename__ = "caudal_medio_de_aguas_corrientes"
    __table_args__ = {"schema": "public"}

    dti_cl_mes = Column(String, primary_key=True)
    dti_cl_estaciones_fluviometricas = Column(String, primary_key=True)

    mes = Column(String)
    dti_cl_aguas_corrientes = Column(String)
    aguas_corrientes = Column(String)
    estaciones_fluviometricas = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)

# ============================
# Lluvia / Evaporación - mensual
# ============================
class CantidadDeAguaCaida(Base):
    __tablename__ = "cantidad_de_agua_caida"
    __table_args__ = {"schema": "public"}

    dti_cl_mes = Column(String, primary_key=True)
    dti_cl_estaciones_meteo = Column(String, primary_key=True)

    mes = Column(String)
    estaciones_meteorologicas_dmc = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)


class EvaporacionRealPorEstacion(Base):
    __tablename__ = "evaporacion_real_por_estacion"
    __table_args__ = {"schema": "public"}

    dti_cl_mes = Column(String, primary_key=True)
    dti_cl_estacion = Column(String, primary_key=True)

    mes = Column(String)
    estacion = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)

# ============================
# Embalses - mensual
# ============================
class VolumenDelEmbalsePorEmbalse(Base):
    __tablename__ = "volumen_del_embalse_por_embalse"
    __table_args__ = {"schema": "public"}

    dti_cl_mes = Column(String, primary_key=True)
    dti_cl_embalse = Column(String, primary_key=True)

    mes = Column(String)
    embalse = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)

# ============================
# Nivometría / Pozos - diaria
# ============================
class AlturaNieveEquivalenteEnAgua(Base):
    __tablename__ = "altura_nieve_equivalente_en_agua"
    __table_args__ = {"schema": "public"}

    dti_cl_dia = Column(BigInteger, primary_key=True)
    dti_cl_t001est_nivo = Column(String, primary_key=True)

    dia = Column(String)
    estaciones_nivometricas = Column(String)
    value = Column(BigInteger)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)


class NivelEstaticoDeAguasSubterraneas(Base):
    __tablename__ = "nivel_estatico_de_aguas_subterraneas"
    __table_args__ = {"schema": "public"}

    dti_cl_dia = Column(BigInteger, primary_key=True)
    dti_cl_t009estacion_pozo = Column(String, primary_key=True)

    dia = Column(String)
    estaciones_pozo = Column(String)
    value = Column(Float)
    flag_codes = Column(BigInteger)
    flags = Column(BigInteger)
