from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ==================== MARCAS ====================
class MarcaBase(BaseModel):
    nombre: str = Field(..., max_length=40)
    nombre_oficial: Optional[str] = Field(None, max_length=80)
    pais_origen: Optional[str] = Field(None, max_length=30)
    notas: Optional[str] = None


class MarcaCreate(MarcaBase):
    pass


class MarcaResponse(MarcaBase):
    id_marca: int
    activo: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True


# ==================== MODELOS ====================
class ModeloBase(BaseModel):
    id_marca: int
    nombre: str = Field(..., max_length=50)
    nombre_comercial: Optional[str] = Field(None, max_length=50)
    generacion: Optional[str] = Field(None, max_length=20)
    tipo_vehiculo: Optional[str] = Field(None, max_length=30)
    ano_inicio_produccion: Optional[int] = None
    ano_fin_produccion: Optional[int] = None
    notas: Optional[str] = None


class ModeloCreate(ModeloBase):
    pass


class ModeloResponse(ModeloBase):
    id_modelo: int
    activo: bool

    class Config:
        from_attributes = True


# ==================== VERSIONES ====================
class VersionBase(BaseModel):
    id_modelo: int
    nombre: str = Field(..., max_length=80)
    motor: Optional[str] = Field(None, max_length=50)
    caballos_fuerza: Optional[int] = None
    transmision: Optional[str] = Field(None, max_length=30)
    traccion: Optional[str] = Field(None, max_length=20)
    carroceria: Optional[str] = Field(None, max_length=20)
    combustible: Optional[str] = Field(None, max_length=20)
    ano_inicio: Optional[int] = None
    ano_fin: Optional[int] = None
    notas: Optional[str] = None


class VersionCreate(VersionBase):
    pass


class VersionResponse(VersionBase):
    id_version: int
    activo: bool

    class Config:
        from_attributes = True


# ==================== TIPOS DE CLIENTE ====================
class TipoClienteBase(BaseModel):
    nombre: str = Field(..., max_length=30)
    descripcion: Optional[str] = Field(None, max_length=100)
    requiere_rfc: bool = True


class TipoClienteCreate(TipoClienteBase):
    pass


class TipoClienteResponse(TipoClienteBase):
    id_tipo_cliente: int
    activo: bool

    class Config:
        from_attributes = True