from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.catalogo import TipoCliente
from app.schemas.catalogo import TipoClienteCreate, TipoClienteResponse

router = APIRouter(prefix="/tipos-cliente", tags=["Catálogos - Tipos de Cliente"])


@router.post("/", response_model=TipoClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_cliente(tipo: TipoClienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de cliente"""
    existing = db.query(TipoCliente).filter(TipoCliente.nombre == tipo.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe ese tipo de cliente")
    
    nuevo_tipo = TipoCliente(**tipo.model_dump())
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return nuevo_tipo


@router.get("/", response_model=List[TipoClienteResponse])
def listar_tipos_cliente(db: Session = Depends(get_db)):
    """Listar todos los tipos de cliente"""
    return db.query(TipoCliente).filter(TipoCliente.activo == True).all()