from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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

@router.get("/{venta_id}", response_model=schemas.Venta)
def read_venta(venta_id: int, db: Session = Depends(get_db)):
    db_venta = venta_service.get_venta(db, venta_id=venta_id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_venta
