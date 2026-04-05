from sqlalchemy import Column, Integer, String, Boolean, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import date


class Marca(Base):
    __tablename__ = "cat_marcas"

    id_marca = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(40), nullable=False, unique=True)
    nombre_oficial = Column(String(80))
    pais_origen = Column(String(30))
    activo = Column(Boolean, nullable=False, default=True)
    #fecha_registro = Column(Date, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=date.today)  # ← CAMBIA ESTA LÍNEA
    notas = Column(Text)

    # Relaciones
    modelos = relationship("Modelo", back_populates="marca", cascade="all, delete-orphan")


class Modelo(Base):
    __tablename__ = "cat_modelos"

    id_modelo = Column(Integer, primary_key=True, autoincrement=True)
    id_marca = Column(Integer, ForeignKey("cat_marcas.id_marca"), nullable=False)
    nombre = Column(String(50), nullable=False)
    nombre_comercial = Column(String(50))
    generacion = Column(String(20))
    tipo_vehiculo = Column(String(30))
    ano_inicio_produccion = Column(Integer)
    ano_fin_produccion = Column(Integer)
    activo = Column(Boolean, nullable=False, default=True)
    notas = Column(Text)

    # Relaciones
    marca = relationship("Marca", back_populates="modelos")
    versiones = relationship("Version", back_populates="modelo", cascade="all, delete-orphan")


class Version(Base):
    __tablename__ = "cat_versiones"

    id_version = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo = Column(Integer, ForeignKey("cat_modelos.id_modelo"), nullable=False)
    nombre = Column(String(80), nullable=False)
    motor = Column(String(50))
    caballos_fuerza = Column(Integer)
    transmision = Column(String(30))
    traccion = Column(String(20))
    carroceria = Column(String(20))
    combustible = Column(String(20))
    ano_inicio = Column(Integer)
    ano_fin = Column(Integer)
    activo = Column(Boolean, nullable=False, default=True)
    notas = Column(Text)

    # Relaciones
    modelo = relationship("Modelo", back_populates="versiones")


class TipoCliente(Base):
    __tablename__ = "cat_tipos_cliente"

    id_tipo_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False, unique=True)
    descripcion = Column(String(100))
    requiere_rfc = Column(Boolean, nullable=False, default=True)
    activo = Column(Boolean, nullable=False, default=True)

    # Relaciones
    clientes = relationship("Cliente", back_populates="tipo_cliente")