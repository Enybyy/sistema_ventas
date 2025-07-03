from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from services import producto_service
from app.schemas import Producto, ProductoCreate, ProductoUpdate

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Producto, status_code=201)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return producto_service.create_producto(db=db, producto=producto)


@router.get("/", response_model=List[Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = producto_service.get_productos(db, skip=skip, limit=limit)
    return productos


@router.get("/{producto_id}", response_model=Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = producto_service.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@router.patch("/{producto_id}", response_model=Producto)
def update_producto(
    producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)
):
    db_producto = producto_service.update_producto(
        db=db, producto_id=producto_id, producto_update=producto
    )
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto
