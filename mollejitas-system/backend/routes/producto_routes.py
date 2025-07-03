from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from services import producto_service
from app.database import SessionLocal

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Producto, status_code=201)
def create_producto_endpoint(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return producto_service.create_producto(db=db, producto=producto)

@router.get("/", response_model=List[schemas.Producto])
def read_productos_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = producto_service.get_productos(db, skip=skip, limit=limit)
    return productos

@router.get("/{producto_id}", response_model=schemas.Producto)
def read_producto_endpoint(producto_id: int, db: Session = Depends(get_db)):
    db_producto = producto_service.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto
