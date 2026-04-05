from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class VehiculoDespiece(Base):
    __tablename__ = "vehiculos_despiece"

    id_vehiculo = Column(Integer, primary_key=True, autoincrement=True)
    folio_entrada = Column(String(30), nullable=False, unique=True)
    id_version = Column(Integer, ForeignKey("cat_versiones.id_version"), nullable=False)
    ano_fabricacion = Column(Integer, nullable=False)
    color = Column(String(30))
    kilometraje = Column(Integer)
    vin = Column(String(17), unique=True)
    placa = Column(String(10))
    fecha_ingreso = Column(Date, nullable=False)
    fecha_inicio_despiece = Column(Date)
    fecha_termino_despiece = Column(Date)
    costo_compra = Column(Float)
    estado = Column(String(20), nullable=False, default="Registrado")
    notas = Column(Text)

    # Relaciones
    piezas = relationship("PiezaUsada", back_populates="vehiculo_procedencia")


class PiezaUsada(Base):
    __tablename__ = "piezas_usadas"

    id_pieza = Column(Integer, primary_key=True, autoincrement=True)
    id_vehiculo_procedencia = Column(Integer, ForeignKey("vehiculos_despiece.id_vehiculo"))
    id_version = Column(Integer, ForeignKey("cat_versiones.id_version"))
    nombre = Column(String(100), nullable=False)
    numero_parte_oem = Column(String(50))
    condicion = Column(String(30), nullable=False, default="Bueno")
    precio = Column(Float, nullable=False)
    precio_oferta = Column(Float)
    garantia_dias = Column(Integer)
    ubicacion = Column(String(50))
    fecha_disponible = Column(Date, nullable=False)
    fecha_venta = Column(Date)
    notas = Column(Text)

    # Relaciones
    vehiculo_procedencia = relationship("VehiculoDespiece", back_populates="piezas")
    compatibilidades = relationship("Compatibilidad", back_populates="pieza", cascade="all, delete-orphan")
    detalles_venta = relationship("VentaDetalle", back_populates="pieza")


class Compatibilidad(Base):
    __tablename__ = "compatibilidad_piezas"

    id_compatibilidad = Column(Integer, primary_key=True, autoincrement=True)
    id_pieza = Column(Integer, ForeignKey("piezas_usadas.id_pieza"), nullable=False)
    id_version = Column(Integer, ForeignKey("cat_versiones.id_version"), nullable=False)
    notas = Column(Text)

    # Relaciones
    pieza = relationship("PiezaUsada", back_populates="compatibilidades")
    version = relationship("Version")