from sqlalchemy.orm import Session
from models.producto import Producto as ProductoModel
from app.schemas import ProductoCreate

def get_producto(db: Session, producto_id: int):
    return db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductoModel).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate):
    db_producto = ProductoModel(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto
