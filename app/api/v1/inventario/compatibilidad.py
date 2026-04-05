from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.inventario import Compatibilidad, PiezaUsada
from app.models.catalogo import Version
from app.schemas.inventario import CompatibilidadCreate, CompatibilidadResponse

router = APIRouter(prefix="/compatibilidad", tags=["Inventario - Compatibilidad"])


@router.post("/", response_model=CompatibilidadResponse, status_code=status.HTTP_201_CREATED)
def crear_compatibilidad(comp: CompatibilidadCreate, db: Session = Depends(get_db)):
    """Registrar compatibilidad de una pieza con una versión"""
    
    # Verificar que la pieza existe
    pieza = db.query(PiezaUsada).filter(PiezaUsada.id_pieza == comp.id_pieza).first()
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    # Verificar que la versión existe
    version = db.query(Version).filter(Version.id_version == comp.id_version).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    
    # Verificar que no exista duplicado
    existing = db.query(Compatibilidad).filter(
        Compatibilidad.id_pieza == comp.id_pieza,
        Compatibilidad.id_version == comp.id_version
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Esta compatibilidad ya existe")
    
    nueva_comp = Compatibilidad(**comp.model_dump())
    db.add(nueva_comp)
    db.commit()
    db.refresh(nueva_comp)
    return nueva_comp


@router.get("/pieza/{id_pieza}", response_model=List[CompatibilidadResponse])
def compatibilidades_por_pieza(id_pieza: int, db: Session = Depends(get_db)):
    """Obtener todas las compatibilidades de una pieza"""
    return db.query(Compatibilidad).filter(Compatibilidad.id_pieza == id_pieza).all()


@router.delete("/{id_compatibilidad}")
def eliminar_compatibilidad(id_compatibilidad: int, db: Session = Depends(get_db)):
    """Eliminar una compatibilidad"""
    comp = db.query(Compatibilidad).filter(Compatibilidad.id_compatibilidad == id_compatibilidad).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Compatibilidad no encontrada")
    
    db.delete(comp)
    db.commit()
    return {"message": "Compatibilidad eliminada correctamente"}