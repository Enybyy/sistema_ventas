from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float
    costo_unitario: float
    categoria: str

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True
