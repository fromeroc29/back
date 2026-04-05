from app.schemas.catalogo import (
    MarcaBase, MarcaCreate, MarcaResponse,
    ModeloBase, ModeloCreate, ModeloResponse,
    VersionBase, VersionCreate, VersionResponse,
    TipoClienteBase, TipoClienteCreate, TipoClienteResponse
)
from app.schemas.inventario import (
    VehiculoBase, VehiculoCreate, VehiculoResponse,
    PiezaBase, PiezaCreate, PiezaResponse,
    CompatibilidadBase, CompatibilidadCreate, CompatibilidadResponse
)
from app.schemas.ventas import (
    ClienteBase, ClienteCreate, ClienteResponse,
    VentaBase, VentaCreate, VentaResponse,
    VentaDetalleBase, VentaDetalleCreate, VentaDetalleResponse
)

__all__ = [
    "MarcaBase", "MarcaCreate", "MarcaResponse",
    "ModeloBase", "ModeloCreate", "ModeloResponse",
    "VersionBase", "VersionCreate", "VersionResponse",
    "TipoClienteBase", "TipoClienteCreate", "TipoClienteResponse",
    "VehiculoBase", "VehiculoCreate", "VehiculoResponse",
    "PiezaBase", "PiezaCreate", "PiezaResponse",
    "CompatibilidadBase", "CompatibilidadCreate", "CompatibilidadResponse",
    "ClienteBase", "ClienteCreate", "ClienteResponse",
    "VentaBase", "VentaCreate", "VentaResponse",
    "VentaDetalleBase", "VentaDetalleCreate", "VentaDetalleResponse",
]