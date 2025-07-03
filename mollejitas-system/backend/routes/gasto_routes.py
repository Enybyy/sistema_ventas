from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app import schemas
from services import gasto_service
from app.dependencies import get_db

router = APIRouter(
    prefix="/gastos",
    tags=["gastos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Gasto)
def create_gasto(gasto: schemas.GastoCreate, db: Session = Depends(get_db)):
    return gasto_service.create_gasto(db=db, gasto=gasto)

@router.get("/", response_model=List[schemas.Gasto])
def read_gastos(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    categoria: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    gastos = gasto_service.get_gastos(
        db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, categoria=categoria, skip=skip, limit=limit
    )
    return gastos

@router.get("/{gasto_id}", response_model=schemas.Gasto)
def read_gasto(gasto_id: int, db: Session = Depends(get_db)):
    db_gasto = gasto_service.get_gasto(db, gasto_id=gasto_id)
    if db_gasto is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return db_gasto

@router.patch("/{gasto_id}", response_model=schemas.Gasto)
def update_gasto(gasto_id: int, gasto: schemas.GastoUpdate, db: Session = Depends(get_db)):
    db_gasto = gasto_service.update_gasto(db, gasto_id=gasto_id, gasto=gasto)
    if db_gasto is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return db_gasto

@router.delete("/{gasto_id}", response_model=schemas.Gasto)
def delete_gasto(gasto_id: int, db: Session = Depends(get_db)):
    db_gasto = gasto_service.delete_gasto(db, gasto_id=gasto_id)
    if db_gasto is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return db_gasto
