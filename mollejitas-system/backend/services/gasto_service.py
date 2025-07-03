from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import gasto as gasto_model
from app import schemas
from typing import List, Optional
from datetime import date

def create_gasto(db: Session, gasto: schemas.GastoCreate) -> models.Gasto:
    db_gasto = models.Gasto(**gasto.dict())
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

def get_gasto(db: Session, gasto_id: int) -> Optional[models.Gasto]:
    return db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()

def get_gastos(
    db: Session, 
    fecha_inicio: Optional[date] = None, 
    fecha_fin: Optional[date] = None, 
    categoria: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Gasto]:
    query = db.query(models.Gasto)

    if fecha_inicio:
        query = query.filter(models.Gasto.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(models.Gasto.fecha <= fecha_fin)
    if categoria:
        query = query.filter(models.Gasto.categoria.ilike(f"%{categoria}%"))

    return query.offset(skip).limit(limit).all()

def update_gasto(db: Session, gasto_id: int, gasto: schemas.GastoUpdate) -> Optional[models.Gasto]:
    db_gasto = get_gasto(db, gasto_id)
    if not db_gasto:
        return None

    update_data = gasto.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_gasto, key, value)

    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

def delete_gasto(db: Session, gasto_id: int) -> Optional[models.Gasto]:
    db_gasto = get_gasto(db, gasto_id)
    if not db_gasto:
        return None
    
    db.delete(db_gasto)
    db.commit()
    return db_gasto
