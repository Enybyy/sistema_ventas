from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.proveedor import Proveedor as ProveedorModel
from app.schemas import ProveedorCreate, ProveedorUpdate

def get_proveedor(db: Session, proveedor_id: int) -> Optional[ProveedorModel]:
    return db.query(ProveedorModel).filter(ProveedorModel.id == proveedor_id).first()

def get_proveedor_by_nombre(db: Session, nombre: str) -> Optional[ProveedorModel]:
    return db.query(ProveedorModel).filter(ProveedorModel.nombre == nombre).first()

def get_proveedores(db: Session, skip: int = 0, limit: int = 100) -> List[ProveedorModel]:
    return db.query(ProveedorModel).offset(skip).limit(limit).all()

def create_proveedor(db: Session, proveedor: ProveedorCreate) -> ProveedorModel:
    db_proveedor_existente = get_proveedor_by_nombre(db, nombre=proveedor.nombre)
    if db_proveedor_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El proveedor con el nombre '{proveedor.nombre}' ya existe."
        )
    db_proveedor = ProveedorModel(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def update_proveedor(db: Session, proveedor_id: int, proveedor_update: ProveedorUpdate) -> Optional[ProveedorModel]:
    db_proveedor = get_proveedor(db, proveedor_id)
    if not db_proveedor:
        return None

    update_data = proveedor_update.model_dump(exclude_unset=True)
    
    if "nombre" in update_data and update_data["nombre"] != db_proveedor.nombre:
        db_proveedor_existente = get_proveedor_by_nombre(db, nombre=update_data["nombre"])
        if db_proveedor_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El proveedor con el nombre '{update_data['nombre']}' ya existe."
            )

    for key, value in update_data.items():
        setattr(db_proveedor, key, value)

    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def delete_proveedor(db: Session, proveedor_id: int) -> Optional[ProveedorModel]:
    db_proveedor = get_proveedor(db, proveedor_id)
    if not db_proveedor:
        return None
    db.delete(db_proveedor)
    db.commit()
    return db_proveedor
