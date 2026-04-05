from pydantic import BaseModel, Field
from datetime import date,datetime
from typing import Optional


# ==================== VEHÍCULOS DESPIECE ====================
class VehiculoBase(BaseModel):
    folio_entrada: str = Field(..., max_length=30)
    id_version: int
    ano_fabricacion: int = Field(..., ge=1980, le=2026)
    color: Optional[str] = Field(None, max_length=30)
    kilometraje: Optional[int] = Field(None, ge=0)
    vin: Optional[str] = Field(None, max_length=17)
    placa: Optional[str] = Field(None, max_length=10)
    fecha_ingreso: date
    fecha_inicio_despiece: Optional[date] = None
    fecha_termino_despiece: Optional[date] = None
    costo_compra: Optional[float] = Field(None, ge=0)
    estado: str = Field(default="Registrado", max_length=20)
    notas: Optional[str] = None


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoResponse(VehiculoBase):
    id_vehiculo: int

    class Config:
        from_attributes = True


# ==================== PIEZAS USADAS ====================
class PiezaBase(BaseModel):
    id_vehiculo_procedencia: Optional[int] = None
    id_version: Optional[int] = None
    nombre: str = Field(..., max_length=100)
    numero_parte_oem: Optional[str] = Field(None, max_length=50)
    condicion: str = Field(default="Bueno", max_length=30)
    precio: float = Field(..., ge=0)
    precio_oferta: Optional[float] = Field(None, ge=0)
    garantia_dias: Optional[int] = Field(None, ge=0)
    ubicacion: Optional[str] = Field(None, max_length=50)
    fecha_disponible: date
    notas: Optional[str] = None


class PiezaCreate(PiezaBase):
    pass


class PiezaResponse(PiezaBase):
    id_pieza: int
    fecha_venta: Optional[date] = None

    class Config:
        from_attributes = True


# ==================== COMPATIBILIDAD ====================
class CompatibilidadBase(BaseModel):
    id_pieza: int
    id_version: int
    notas: Optional[str] = None


class CompatibilidadCreate(CompatibilidadBase):
    pass


class CompatibilidadResponse(CompatibilidadBase):
    id_compatibilidad: int

    class Config:
        from_attributes = True