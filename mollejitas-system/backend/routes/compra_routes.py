from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.dependencies import get_db
from services import compra_service

router = APIRouter(
    prefix="/compras",
    tags=["compras"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.Compra])
def read_compras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las compras.
    """
    compras = compra_service.get_compras(db, skip=skip, limit=limit)
    return compras


@router.post("/", response_model=schemas.Compra, status_code=201)
def create_compra(compra: schemas.CompraCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva compra y actualiza el stock de los productos correspondientes.
    """
    return compra_service.create_compra(db=db, compra=compra)
