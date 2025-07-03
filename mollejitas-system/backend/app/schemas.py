from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

# Esquema para Producto (Base)
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float
    costo_unitario: float
    categoria: str
    stock: Optional[int] = 0

# Esquema para la creación de un Producto (hereda de ProductoBase)
class ProductoCreate(ProductoBase):
    pass

# Esquema para actualizar un Producto (todos los campos son opcionales)
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta: Optional[float] = None
    costo_unitario: Optional[float] = None
    categoria: Optional[str] = None
    stock: Optional[int] = None

# Esquema para leer/retornar un Producto (hereda de ProductoBase)
class Producto(ProductoBase):
    id: int
    stock: int

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
    cliente_nombre: Optional[str] = "Cliente Anónimo"

class VentaCreate(VentaBase):
    detalles: List[DetalleVentaCreate]

class Venta(VentaBase):
    id: int
    fecha: datetime
    total: float
    detalles: List[DetalleVenta] = []

    class Config:
        from_attributes = True

# Esquemas para Gasto
class GastoBase(BaseModel):
    descripcion: str
    monto: float
    categoria: Optional[str] = None
    fecha: Optional[date] = None

class GastoCreate(GastoBase):
    pass

class GastoUpdate(GastoBase):
    pass

class Gasto(GastoBase):
    id: int

    class Config:
        orm_mode = True

# Esquemas para DetalleCompra
class DetalleCompraBase(BaseModel):
    producto_id: int
    cantidad: int
    costo_unitario: float

class DetalleCompraCreate(DetalleCompraBase):
    pass

class DetalleCompra(DetalleCompraBase):
    id: int
    compra_id: int

    class Config:
        from_attributes = True

# Esquemas para Compra
class CompraBase(BaseModel):
    proveedor: str | None = None
    detalles: list[DetalleCompraCreate]

class CompraCreate(CompraBase):
    pass

class Compra(CompraBase):
    id: int
    fecha: datetime
    total: float
    detalles: List[DetalleCompra] = []

    class Config:
        from_attributes = True


# Esquemas para Reportes
class ReporteRankingProducto(BaseModel):
    producto: Producto
    cantidad_total_vendida: int

    class Config:
        orm_mode = True


class ReporteGanancias(BaseModel):
    total_ventas: float
    costo_total: float
    ganancia_neta: float
