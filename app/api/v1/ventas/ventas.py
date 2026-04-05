from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.ventas import Venta, VentaDetalle, Cliente
from app.models.inventario import PiezaUsada
from app.schemas.ventas import VentaCreate, VentaResponse, VentaDetalleCreate

router = APIRouter(prefix="/ventas", tags=["Ventas - Ventas"])


@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    """Registrar una nueva venta"""
    
    # Verificar que el cliente existe
    cliente = db.query(Cliente).filter(Cliente.id_cliente == venta.id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    nueva_venta = Venta(**venta.model_dump())
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta


@router.post("/{id_venta}/detalles")
def agregar_detalle_venta(id_venta: int, detalle: VentaDetalleCreate, db: Session = Depends(get_db)):
    """Agregar una pieza a una venta"""
    
    # Verificar que la venta existe
    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    # Verificar que la pieza existe y está disponible
    pieza = db.query(PiezaUsada).filter(PiezaUsada.id_pieza == detalle.id_pieza).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    if pieza.fecha_venta is not None:
        raise HTTPException(status_code=400, detail="La pieza ya fue vendida")
    
    # Crear detalle
    nuevo_detalle = VentaDetalle(**detalle.model_dump())
    db.add(nuevo_detalle)
    
    # Marcar pieza como vendida
    pieza.fecha_venta = date.today()
    
    db.commit()
    
    return {"message": "Pieza agregada a la venta correctamente"}


@router.get("/", response_model=List[VentaResponse])
def listar_ventas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Listar ventas con filtro opcional por fechas"""
    query = db.query(Venta)
    
    if fecha_desde:
        query = query.filter(Venta.fecha_venta >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Venta.fecha_venta <= fecha_hasta)
    
    return query.order_by(Venta.fecha_venta.desc()).offset(skip).limit(limit).all()


@router.get("/{id_venta}", response_model=VentaResponse)
def obtener_venta(id_venta: int, db: Session = Depends(get_db)):
    """Obtener una venta por ID"""
    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta