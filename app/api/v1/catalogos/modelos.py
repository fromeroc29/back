from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.catalogo import Modelo, Marca
from app.schemas.catalogo import ModeloCreate, ModeloResponse

router = APIRouter(prefix="/modelos", tags=["Catálogos - Modelos"])


@router.post("/", response_model=ModeloResponse, status_code=status.HTTP_201_CREATED)
def crear_modelo(modelo: ModeloCreate, db: Session = Depends(get_db)):
    """Crear un nuevo modelo"""
    # Verificar que la marca existe
    marca = db.query(Marca).filter(Marca.id_marca == modelo.id_marca).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    # Verificar que no exista duplicado
    existing = db.query(Modelo).filter(
        Modelo.id_marca == modelo.id_marca,
        Modelo.nombre == modelo.nombre
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe ese modelo para esta marca")
    
    nuevo_modelo = Modelo(**modelo.model_dump())
    db.add(nuevo_modelo)
    db.commit()
    db.refresh(nuevo_modelo)
    return nuevo_modelo


@router.get("/", response_model=List[ModeloResponse])
def listar_modelos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    id_marca: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar modelos con filtro opcional por marca"""
    query = db.query(Modelo)
    if id_marca:
        query = query.filter(Modelo.id_marca == id_marca)
    return query.offset(skip).limit(limit).all()


@router.get("/{id_modelo}", response_model=ModeloResponse)
def obtener_modelo(id_modelo: int, db: Session = Depends(get_db)):
    """Obtener un modelo por ID"""
    modelo = db.query(Modelo).filter(Modelo.id_modelo == id_modelo).first()
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    return modelo


@router.put("/{id_modelo}", response_model=ModeloResponse)
def actualizar_modelo(id_modelo: int, modelo_data: ModeloCreate, db: Session = Depends(get_db)):
    """Actualizar un modelo"""
    modelo = db.query(Modelo).filter(Modelo.id_modelo == id_modelo).first()
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    
    for key, value in modelo_data.model_dump().items():
        setattr(modelo, key, value)
    
    db.commit()
    db.refresh(modelo)
    return modelo


@router.delete("/{id_modelo}")
def eliminar_modelo(id_modelo: int, db: Session = Depends(get_db)):
    """Eliminar un modelo (borrado lógico)"""
    modelo = db.query(Modelo).filter(Modelo.id_modelo == id_modelo).first()
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    
    modelo.activo = False
    db.commit()
    return {"message": "Modelo desactivado correctamente"}