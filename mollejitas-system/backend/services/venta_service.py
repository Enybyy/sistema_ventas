from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.venta import Venta, DetalleVenta
from models.producto import Producto
from app.schemas import VentaCreate

def create_venta(db: Session, venta: VentaCreate) -> Venta:
    total_venta = 0
    detalles_venta_obj = []
    productos_a_actualizar = []

    # 1. Validar productos y stock en un solo bucle
    for item in venta.detalles:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {item.producto_id} no encontrado",
            )
        if producto.stock < item.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, solicitado: {item.cantidad}",
            )

        subtotal_item = producto.precio_venta * item.cantidad
        total_venta += subtotal_item

        # Guardar referencia para actualizar stock después
        productos_a_actualizar.append({"producto": producto, "cantidad_vendida": item.cantidad})

        # Crear objeto DetalleVenta
        detalle_obj = DetalleVenta(
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio_venta,
            subtotal=subtotal_item,
        )
        detalles_venta_obj.append(detalle_obj)

    # 2. Crear la Venta y asociar sus detalles
    db_venta = Venta(
        cliente_nombre=venta.cliente_nombre,
        total=total_venta
    )
    db_venta.detalles = detalles_venta_obj
    db.add(db_venta)

    # 3. Actualizar el stock de los productos involucrados
    for item_actualizar in productos_a_actualizar:
        producto = item_actualizar["producto"]
        producto.stock -= item_actualizar["cantidad_vendida"]
        db.add(producto)

    # 4. Confirmar todos los cambios en la base de datos de forma atómica
    db.commit()
    db.refresh(db_venta)
    return db_venta

def get_venta(db: Session, venta_id: int) -> Optional[Venta]:
    return db.query(Venta).filter(Venta.id == venta_id).first()

def get_ventas(db: Session, skip: int = 0, limit: int = 100) -> List[Venta]:
    return db.query(Venta).offset(skip).limit(limit).all()
