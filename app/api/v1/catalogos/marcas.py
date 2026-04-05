from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.catalogo import Marca
from app.schemas.catalogo import MarcaCreate, MarcaResponse

router = APIRouter(prefix="/marcas", tags=["Catálogos - Marcas"])


@router.post("/", response_model=MarcaResponse, status_code=status.HTTP_201_CREATED)
def crear_marca(marca: MarcaCreate, db: Session = Depends(get_db)):
    """Crear una nueva marca"""
    existing = db.query(Marca).filter(Marca.nombre == marca.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una marca con ese nombre")
    

    nueva_marca = Marca(
        nombre=marca.nombre,
        nombre_oficial=marca.nombre_oficial,
        pais_origen=marca.pais_origen,
        activo=True,
        fecha_registro=date.today(),  # ← Asignar aquí
        notas=marca.notas
    )
    pp = vars(nueva_marca)
    print("************************************************",pp)
    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)
    
    return nueva_marca


@router.get("/", response_model=List[MarcaResponse])
def listar_marcas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar todas las marcas"""
    query = db.query(Marca)
    if activo is not None:
        query = query.filter(Marca.activo == activo)
    return query.offset(skip).limit(limit).all()


@router.get("/{id_marca}", response_model=MarcaResponse)
def obtener_marca(id_marca: int, db: Session = Depends(get_db)):
    """Obtener una marca por ID"""
    marca = db.query(Marca).filter(Marca.id_marca == id_marca).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca


@router.put("/{id_marca}", response_model=MarcaResponse)
def actualizar_marca(id_marca: int, marca_data: MarcaCreate, db: Session = Depends(get_db)):
    """Actualizar una marca"""
    marca = db.query(Marca).filter(Marca.id_marca == id_marca).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    for key, value in marca_data.model_dump().items():
        setattr(marca, key, value)
    
    db.commit()
    db.refresh(marca)
    return marca


@router.delete("/{id_marca}")
def eliminar_marca(id_marca: int, db: Session = Depends(get_db)):
    """Eliminar una marca (borrado lógico)"""
    marca = db.query(Marca).filter(Marca.id_marca == id_marca).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    marca.activo = False
    db.commit()
    return {"message": "Marca desactivada correctamente"}