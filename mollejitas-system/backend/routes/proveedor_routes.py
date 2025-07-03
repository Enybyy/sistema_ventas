from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import Proveedor, ProveedorCreate, ProveedorUpdate
from app.dependencies import get_db
from services import proveedor_service

router = APIRouter(
    prefix="/proveedores",
    tags=["proveedores"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Proveedor, status_code=status.HTTP_201_CREATED)
def create_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    return proveedor_service.create_proveedor(db=db, proveedor=proveedor)

@router.get("/", response_model=List[Proveedor])
def read_proveedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proveedores = proveedor_service.get_proveedores(db, skip=skip, limit=limit)
    return proveedores

@router.get("/{proveedor_id}", response_model=Proveedor)
def read_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = proveedor_service.get_proveedor(db, proveedor_id=proveedor_id)
    if db_proveedor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return db_proveedor

@router.patch("/{proveedor_id}", response_model=Proveedor)
def update_proveedor(proveedor_id: int, proveedor: ProveedorUpdate, db: Session = Depends(get_db)):
    db_proveedor = proveedor_service.update_proveedor(db=db, proveedor_id=proveedor_id, proveedor_update=proveedor)
    if db_proveedor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return db_proveedor

@router.delete("/{proveedor_id}", response_model=Proveedor)
def delete_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = proveedor_service.delete_proveedor(db, proveedor_id=proveedor_id)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor
