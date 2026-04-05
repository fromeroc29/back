from app.models.catalogo import Marca, Modelo, Version, TipoCliente
from app.models.inventario import VehiculoDespiece, PiezaUsada, Compatibilidad
from app.models.ventas import Cliente, Venta, VentaDetalle

__all__ = [
    "Marca",
    "Modelo",
    "Version",
    "TipoCliente",
    "VehiculoDespiece",
    "PiezaUsada",
    "Compatibilidad",
    "Cliente",
    "Venta",
    "VentaDetalle",
]