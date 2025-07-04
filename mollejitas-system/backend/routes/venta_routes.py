from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from services import venta_service
from app import schemas
from app.dependencies import get_db

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Venta)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    try:
        return venta_service.create_venta(db=db, venta=venta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Venta])
def read_ventas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ventas = venta_service.get_ventas(db, skip=skip, limit=limit)
    return ventas

@router.get("/reportes/ganancias", response_model=schemas.ReporteGanancias)
def get_ganancias_reporte(fecha_inicio: date, fecha_fin: date, db: Session = Depends(get_db)):
    """
    Obtiene un reporte de ganancias (ventas, costos, ganancia neta) en un rango de fechas.
    """
    return venta_service.get_reporte_ganancias(db=db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@router.get("/reportes/ranking-productos", response_model=List[schemas.ReporteRankingProducto])
def get_ranking_productos(limit: int = 10, db: Session = Depends(get_db)):
    """
    Obtiene un ranking de los productos más vendidos.
    """
    return venta_service.get_ranking_productos_vendidos(db=db, limit=limit)


@router.get("/{venta_id}", response_model=schemas.Venta)
def read_venta(venta_id: int, db: Session = Depends(get_db)):
    db_venta = venta_service.get_venta(db, venta_id=venta_id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_venta
