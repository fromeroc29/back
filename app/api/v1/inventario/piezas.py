from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.catalogo import Version
from app.models.inventario import PiezaUsada, VehiculoDespiece, Compatibilidad
from app.schemas.inventario import PiezaCreate, PiezaResponse

router = APIRouter(prefix="/piezas", tags=["Inventario - Piezas"])


@router.post("/", response_model=PiezaResponse, status_code=status.HTTP_201_CREATED)
def crear_pieza(pieza: PiezaCreate, db: Session = Depends(get_db)):
    """Registrar una nueva pieza en inventario"""
    
    # Validar origen
    if pieza.id_vehiculo_procedencia is None and pieza.id_version is None:
        raise HTTPException(
            status_code=400, 
            detail="Debe especificar id_vehiculo_procedencia o id_version"
        )
    
    # Validar vehículo
    if pieza.id_vehiculo_procedencia:
        vehiculo = db.query(VehiculoDespiece).filter(
            VehiculoDespiece.id_vehiculo == pieza.id_vehiculo_procedencia
        ).first()
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo de procedencia no encontrado")
    
    # Validar versión
    if pieza.id_version:
        version = db.query(Version).filter(Version.id_version == pieza.id_version).first()
        if not version:
            raise HTTPException(status_code=404, detail="Versión no encontrada")
    
    nueva_pieza = PiezaUsada(**pieza.model_dump())
    db.add(nueva_pieza)
    db.commit()
    db.refresh(nueva_pieza)
    return nueva_pieza


@router.get("/", response_model=List[PiezaResponse])
def listar_piezas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    disponibles: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar piezas con filtro opcional por disponibilidad"""
    query = db.query(PiezaUsada)
    
    if disponibles is True:
        query = query.filter(PiezaUsada.fecha_venta.is_(None))
    elif disponibles is False:
        query = query.filter(PiezaUsada.fecha_venta.isnot(None))
    
    return query.offset(skip).limit(limit).all()


@router.get("/buscar/{texto}", response_model=List[PiezaResponse])
def buscar_piezas(texto: str, db: Session = Depends(get_db)):
    """Buscar piezas disponibles por nombre"""
    piezas = db.query(PiezaUsada).filter(
        PiezaUsada.fecha_venta.is_(None),
        PiezaUsada.nombre.ilike(f"%{texto}%")
    ).all()
    return piezas


@router.get("/compatibles/{id_version}", response_model=List[PiezaResponse])
def piezas_compatibles_con_version(id_version: int, db: Session = Depends(get_db)):
    """Buscar piezas compatibles con una versión de auto"""
    
    compatibles_subquery = db.query(Compatibilidad.id_pieza).filter(
        Compatibilidad.id_version == id_version
    )
    
    piezas = db.query(PiezaUsada).filter(
        PiezaUsada.fecha_venta.is_(None),
        (PiezaUsada.id_version == id_version) | 
        (PiezaUsada.id_pieza.in_(compatibles_subquery))
    ).distinct().all()
    
    return piezas


@router.get("/{id_pieza}", response_model=PiezaResponse)
def obtener_pieza(id_pieza: int, db: Session = Depends(get_db)):
    """Obtener una pieza por ID"""
    pieza = db.query(PiezaUsada).filter(PiezaUsada.id_pieza == id_pieza).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    return pieza


@router.put("/{id_pieza}", response_model=PiezaResponse)
def actualizar_pieza(id_pieza: int, pieza_data: PiezaCreate, db: Session = Depends(get_db)):
    """Actualizar datos de una pieza"""
    pieza = db.query(PiezaUsada).filter(PiezaUsada.id_pieza == id_pieza).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    for key, value in pieza_data.model_dump().items():
        setattr(pieza, key, value)
    
    db.commit()
    db.refresh(pieza)
    return pieza


@router.patch("/{id_pieza}/precio")
def actualizar_precio(id_pieza: int, nuevo_precio: float = Query(..., ge=0), db: Session = Depends(get_db)):
    """Actualizar solo el precio de una pieza"""
    pieza = db.query(PiezaUsada).filter(PiezaUsada.id_pieza == id_pieza).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    if pieza.fecha_venta is not None:
        raise HTTPException(status_code=400, detail="No se puede modificar precio de una pieza vendida")
    
    pieza.precio = nuevo_precio
    db.commit()
    return {"id_pieza": id_pieza, "nuevo_precio": nuevo_precio}


@router.delete("/{id_pieza}")
def eliminar_pieza(id_pieza: int, db: Session = Depends(get_db)):
    """Eliminar una pieza (solo si no ha sido vendida)"""
    pieza = db.query(PiezaUsada).filter(PiezaUsada.id_pieza == id_pieza).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    if pieza.fecha_venta is not None:
        raise HTTPException(status_code=400, detail="No se puede eliminar una pieza vendida")
    
    db.delete(pieza)
    db.commit()
    return {"message": "Pieza eliminada correctamente"}