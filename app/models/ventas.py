from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    id_tipo_cliente = Column(Integer, ForeignKey("cat_tipos_cliente.id_tipo_cliente"), nullable=False)
    nombre = Column(String(100), nullable=False)
    rfc = Column(String(13))
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(Text)
    notas = Column(Text)
    fecha_registro = Column(Date, nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    # Relaciones
    tipo_cliente = relationship("TipoCliente", back_populates="clientes")
    ventas = relationship("Venta", back_populates="cliente", cascade="all, delete-orphan")


class Venta(Base):
    __tablename__ = "ventas"

    id_venta = Column(Integer, primary_key=True, autoincrement=True)
    folio = Column(String(30), nullable=False, unique=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    fecha_venta = Column(Date, nullable=False)
    subtotal = Column(Float, nullable=False)
    iva = Column(Float, nullable=False, default=0)
    total = Column(Float, nullable=False)
    metodo_pago = Column(String(30))
    notas = Column(Text)

    # Relaciones
    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("VentaDetalle", back_populates="venta", cascade="all, delete-orphan")


class VentaDetalle(Base):
    __tablename__ = "ventas_detalle"

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"), nullable=False)
    id_pieza = Column(Integer, ForeignKey("piezas_usadas.id_pieza"), nullable=False)
    precio_unitario = Column(Float, nullable=False)

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    pieza = relationship("PiezaUsada", back_populates="detalles_venta")