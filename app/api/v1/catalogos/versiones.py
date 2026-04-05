from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.catalogo import Version, Modelo
from app.schemas.catalogo import VersionCreate, VersionResponse

router = APIRouter(prefix="/versiones", tags=["Catálogos - Versiones"])


@router.post("/", response_model=VersionResponse, status_code=status.HTTP_201_CREATED)
def crear_version(version: VersionCreate, db: Session = Depends(get_db)):
    """Crear una nueva versión"""
    # Verificar que el modelo existe
    modelo = db.query(Modelo).filter(Modelo.id_modelo == version.id_modelo).first()
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    
    nueva_version = Version(**version.model_dump())
    db.add(nueva_version)
    db.commit()
    db.refresh(nueva_version)
    return nueva_version


@router.get("/", response_model=List[VersionResponse])
def listar_versiones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    id_modelo: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar versiones con filtro opcional por modelo"""
    query = db.query(Version)
    if id_modelo:
        query = query.filter(Version.id_modelo == id_modelo)
    return query.offset(skip).limit(limit).all()


@router.get("/{id_version}", response_model=VersionResponse)
def obtener_version(id_version: int, db: Session = Depends(get_db)):
    """Obtener una versión por ID"""
    version = db.query(Version).filter(Version.id_version == id_version).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    return version


@router.put("/{id_version}", response_model=VersionResponse)
def actualizar_version(id_version: int, version_data: VersionCreate, db: Session = Depends(get_db)):
    """Actualizar una versión"""
    version = db.query(Version).filter(Version.id_version == id_version).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    
    for key, value in version_data.model_dump().items():
        setattr(version, key, value)
    
    db.commit()
    db.refresh(version)
    return version


@router.delete("/{id_version}")
def eliminar_version(id_version: int, db: Session = Depends(get_db)):
    """Eliminar una versión (borrado lógico)"""
    version = db.query(Version).filter(Version.id_version == id_version).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    
    version.activo = False
    db.commit()
    return {"message": "Versión desactivada correctamente"}