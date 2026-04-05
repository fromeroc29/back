from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.catalogo import Version
from app.models.inventario import VehiculoDespiece
from app.schemas.inventario import VehiculoCreate, VehiculoResponse

router = APIRouter(prefix="/vehiculos", tags=["Inventario - Vehículos"])


@router.post("/", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
def crear_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo vehículo para despiece"""
    # Verificar que la versión existe
    version = db.query(Version).filter(Version.id_version == vehiculo.id_version).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    
    # Verificar folio único
    existing = db.query(VehiculoDespiece).filter(VehiculoDespiece.folio_entrada == vehiculo.folio_entrada).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un vehículo con ese folio")
    
    nuevo_vehiculo = VehiculoDespiece(**vehiculo.model_dump())
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo


@router.get("/", response_model=List[VehiculoResponse])
def listar_vehiculos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar vehículos con filtro opcional por estado"""
    query = db.query(VehiculoDespiece)
    if estado:
        query = query.filter(VehiculoDespiece.estado == estado)
    return query.offset(skip).limit(limit).all()


@router.get("/{id_vehiculo}", response_model=VehiculoResponse)
def obtener_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    """Obtener un vehículo por ID"""
    vehiculo = db.query(VehiculoDespiece).filter(VehiculoDespiece.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo


@router.put("/{id_vehiculo}", response_model=VehiculoResponse)
def actualizar_vehiculo(id_vehiculo: int, vehiculo_data: VehiculoCreate, db: Session = Depends(get_db)):
    """Actualizar datos de un vehículo"""
    vehiculo = db.query(VehiculoDespiece).filter(VehiculoDespiece.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    for key, value in vehiculo_data.model_dump().items():
        setattr(vehiculo, key, value)
    
    db.commit()
    db.refresh(vehiculo)
    return vehiculo


@router.patch("/{id_vehiculo}/estado")
def cambiar_estado_vehiculo(id_vehiculo: int, estado: str, db: Session = Depends(get_db)):
    """Cambiar el estado de un vehículo"""
    vehiculo = db.query(VehiculoDespiece).filter(VehiculoDespiece.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    estados_validos = ["Registrado", "En despiece", "Desarmado", "En pausa", "Vendido completo", "Chatarra"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado no válido. Opciones: {estados_validos}")
    
    vehiculo.estado = estado
    db.commit()
    return {"message": f"Estado actualizado a '{estado}'", "id_vehiculo": id_vehiculo}