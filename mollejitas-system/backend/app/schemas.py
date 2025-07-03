from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Esquema para Producto (Base)
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float
    costo_unitario: float
    categoria: str

# Esquema para la creación de un Producto (hereda de ProductoBase)
class ProductoCreate(ProductoBase):
    pass

# Esquema para leer/retornar un Producto (hereda de ProductoBase)
class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para DetalleVenta
class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVenta(DetalleVentaBase):
    id: int
    venta_id: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True

# Esquemas para Venta
class VentaBase(BaseModel):
    pass

class VentaCreate(VentaBase):
    detalles: List[DetalleVentaCreate]

class Venta(VentaBase):
    id: int
    fecha: datetime
    total: float
    detalles: List[DetalleVenta] = []

    class Config:
        from_attributes = True
