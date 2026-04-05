from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.catalogo import TipoCliente
from app.models.ventas import Cliente
from app.schemas.ventas import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Ventas - Clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo cliente"""
    
    # Verificar que el tipo de cliente existe
    tipo = db.query(TipoCliente).filter(TipoCliente.id_tipo_cliente == cliente.id_tipo_cliente).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cliente no encontrado")
    
    nuevo_cliente = Cliente(**cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar clientes con búsqueda opcional"""
    query = db.query(Cliente).filter(Cliente.activo == True)
    
    if search:
        query = query.filter(Cliente.nombre.ilike(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()


@router.get("/{id_cliente}", response_model=ClienteResponse)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    """Obtener un cliente por ID"""
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{id_cliente}", response_model=ClienteResponse)
def actualizar_cliente(id_cliente: int, cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Actualizar datos de un cliente"""
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    for key, value in cliente_data.model_dump().items():
        setattr(cliente, key, value)
    
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{id_cliente}")
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    """Eliminar un cliente (borrado lógico)"""
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    cliente.activo = False
    db.commit()
    return {"message": "Cliente desactivado correctamente"}