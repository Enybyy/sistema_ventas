from typing import List, Optional
from sqlalchemy.orm import Session
from models.producto import Producto as ProductoModel
from app.schemas import ProductoCreate, ProductoUpdate

def get_producto(db: Session, producto_id: int) -> Optional[ProductoModel]:
    return db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100) -> List[ProductoModel]:
    return db.query(ProductoModel).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate) -> ProductoModel:
    db_producto = ProductoModel(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_update: ProductoUpdate) -> Optional[ProductoModel]:
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        return None

    update_data = producto_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)

    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto
