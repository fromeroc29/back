from pydantic import BaseModel, Field
from datetime import date,datetime
from typing import Optional


# ==================== CLIENTES ====================
class ClienteBase(BaseModel):
    id_tipo_cliente: int
    nombre: str = Field(..., max_length=100)
    rfc: Optional[str] = Field(None, max_length=13)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = None
    notas: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id_cliente: int
    fecha_registro: date
    activo: bool

    class Config:
        from_attributes = True


# ==================== VENTAS ====================
class VentaBase(BaseModel):
    folio: str = Field(..., max_length=30)
    id_cliente: int
    fecha_venta: date
    subtotal: float = Field(..., ge=0)
    iva: float = Field(default=0, ge=0)
    total: float = Field(..., ge=0)
    metodo_pago: Optional[str] = Field(None, max_length=30)
    notas: Optional[str] = None


class VentaCreate(VentaBase):
    pass


class VentaResponse(VentaBase):
    id_venta: int

    class Config:
        from_attributes = True


# ==================== DETALLE DE VENTAS ====================
class VentaDetalleBase(BaseModel):
    id_venta: int
    id_pieza: int
    precio_unitario: float = Field(..., ge=0)


class VentaDetalleCreate(VentaDetalleBase):
    pass


class VentaDetalleResponse(VentaDetalleBase):
    id_detalle: int

    class Config:
        from_attributes = True