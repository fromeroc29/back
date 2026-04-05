from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict, Any
from datetime import date

from app.core.database import get_db
from app.models.ventas import Venta, VentaDetalle, Cliente
from app.models.inventario import PiezaUsada

router = APIRouter(prefix="/reportes", tags=["Ventas - Reportes"])


@router.get("/ventas-por-mes")
def ventas_por_mes(
    anio: Optional[int] = Query(None, description="Año específico"),
    db: Session = Depends(get_db)
):
    """Reporte de ventas agrupadas por mes"""
    
    resultados = db.query(
        func.extract('year', Venta.fecha_venta).label('anio'),
        func.extract('month', Venta.fecha_venta).label('mes'),
        func.count(Venta.id_venta).label('cantidad_ventas'),
        func.sum(Venta.total).label('total_vendido')
    ).group_by('anio', 'mes').order_by('anio', 'mes')
    
    if anio:
        resultados = resultados.filter(func.extract('year', Venta.fecha_venta) == anio)
    
    # Convertir a lista de diccionarios para serialización JSON
    data = []
    for row in resultados.all():
        data.append({
            "anio": int(row.anio) if row.anio else None,
            "mes": int(row.mes) if row.mes else None,
            "cantidad_ventas": int(row.cantidad_ventas) if row.cantidad_ventas else 0,
            "total_vendido": float(row.total_vendido) if row.total_vendido else 0.0
        })
    
    return data


@router.get("/piezas-mas-vendidas")
def piezas_mas_vendidas(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Top de piezas más vendidas"""
    
    resultados = db.query(
        PiezaUsada.nombre,
        func.count(VentaDetalle.id_detalle).label('veces_vendida'),
        func.avg(VentaDetalle.precio_unitario).label('precio_promedio')
    ).join(
        VentaDetalle, PiezaUsada.id_pieza == VentaDetalle.id_pieza
    ).filter(
        PiezaUsada.fecha_venta.isnot(None)
    ).group_by(
        PiezaUsada.id_pieza, PiezaUsada.nombre
    ).order_by(
        func.count(VentaDetalle.id_detalle).desc()
    ).limit(limit).all()
    
    # Convertir a lista de diccionarios
    data = []
    for row in resultados:
        data.append({
            "nombre": row.nombre,
            "veces_vendida": int(row.veces_vendida) if row.veces_vendida else 0,
            "precio_promedio": float(row.precio_promedio) if row.precio_promedio else 0.0
        })
    
    return data


@router.get("/mejores-clientes")
def mejores_clientes(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Top de clientes que más han comprado"""
    
    resultados = db.query(
        Cliente.nombre,
        func.count(Venta.id_venta).label('total_compras'),
        func.sum(Venta.total).label('total_gastado')
    ).join(
        Venta, Cliente.id_cliente == Venta.id_cliente
    ).filter(
        Cliente.activo == True
    ).group_by(
        Cliente.id_cliente, Cliente.nombre
    ).order_by(
        func.sum(Venta.total).desc()
    ).limit(limit).all()
    
    # Convertir a lista de diccionarios
    data = []
    for row in resultados:
        data.append({
            "nombre": row.nombre,
            "total_compras": int(row.total_compras) if row.total_compras else 0,
            "total_gastado": float(row.total_gastado) if row.total_gastado else 0.0
        })
    
    return data


@router.get("/inventario-valor")
def valor_inventario(db: Session = Depends(get_db)):
    """Valor total del inventario disponible"""
    
    resultado = db.query(
        func.count(PiezaUsada.id_pieza).label('piezas_disponibles'),
        func.sum(PiezaUsada.precio).label('valor_total')
    ).filter(PiezaUsada.fecha_venta.is_(None)).first()
    
    return {
        "piezas_disponibles": int(resultado.piezas_disponibles) if resultado.piezas_disponibles else 0,
        "valor_total": float(resultado.valor_total) if resultado.valor_total else 0.0
    }


@router.get("/ventas-por-dia")
def ventas_por_dia(
    fecha_desde: Optional[date] = Query(None),
    fecha_hasta: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Reporte de ventas agrupadas por día"""
    
    query = db.query(
        Venta.fecha_venta,
        func.count(Venta.id_venta).label('cantidad_ventas'),
        func.sum(Venta.total).label('total_vendido')
    ).group_by(Venta.fecha_venta).order_by(Venta.fecha_venta.desc())
    
    if fecha_desde:
        query = query.filter(Venta.fecha_venta >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Venta.fecha_venta <= fecha_hasta)
    
    resultados = query.limit(30).all()
    
    data = []
    for row in resultados:
        data.append({
            "fecha": row.fecha_venta.isoformat() if row.fecha_venta else None,
            "cantidad_ventas": int(row.cantidad_ventas) if row.cantidad_ventas else 0,
            "total_vendido": float(row.total_vendido) if row.total_vendido else 0.0
        })
    
    return data