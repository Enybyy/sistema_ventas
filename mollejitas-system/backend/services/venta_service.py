from typing import List, Optional
from datetime import date, datetime, time
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.venta import Venta, DetalleVenta
from models.producto import Producto
from models.gasto import Gasto
from app.schemas import VentaCreate, ReporteRankingProducto, ReporteGanancias
from sqlalchemy import func

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
        if producto.stock_actual < item.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock_actual}, solicitado: {item.cantidad}",
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
        producto.stock_actual -= item_actualizar["cantidad_vendida"]
        db.add(producto)

    # 4. Confirmar todos los cambios en la base de datos de forma atómica
    db.commit()
    db.refresh(db_venta)
    return db_venta

def get_venta(db: Session, venta_id: int) -> Optional[Venta]:
    return db.query(Venta).filter(Venta.id == venta_id).first()

def get_ventas(db: Session, skip: int = 0, limit: int = 100) -> List[Venta]:
    return db.query(Venta).offset(skip).limit(limit).all()

def get_ranking_productos_vendidos(db: Session, limit: int = 10) -> List[ReporteRankingProducto]:
    """
    Obtiene un ranking de los productos más vendidos.
    """
    ranking_query = (
        db.query(
            Producto,
            func.sum(DetalleVenta.cantidad).label("cantidad_total_vendida")
        )
        .join(Producto, DetalleVenta.producto_id == Producto.id)
        .group_by(Producto.id)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .limit(limit)
        .all()
    )

    return [
        ReporteRankingProducto(
            producto=producto,
            cantidad_total_vendida=cantidad if cantidad else 0
        )
        for producto, cantidad in ranking_query
    ]

def get_reporte_ganancias(db: Session, fecha_inicio: date, fecha_fin: date) -> ReporteGanancias:
    """
    Calcula las ganancias totales, costos, gastos y ventas en un rango de fechas.
    """
    # Convertir las fechas a datetime para una comparación precisa
    fecha_inicio_dt = datetime.combine(fecha_inicio, time.min)
    fecha_fin_dt = datetime.combine(fecha_fin, time.max)

    # 1. Calcular total de ventas y costos a partir de los detalles de venta
    detalles = (
        db.query(DetalleVenta)
        .join(Venta)
        .filter(Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt))
        .all()
    )
    total_ventas = sum(d.subtotal for d in detalles)
    total_costos = sum(d.producto.costo_unitario * d.cantidad for d in detalles)

    # 2. Calcular total de gastos operativos
    total_gastos = db.query(func.sum(Gasto.monto)).filter(
        Gasto.fecha.between(fecha_inicio_dt, fecha_fin_dt)
    ).scalar() or 0.0

    # 3. Calcular ganancia neta
    ganancia_neta = total_ventas - total_costos - total_gastos

    return ReporteGanancias(
        total_ventas=total_ventas,
        total_costos=total_costos,
        total_gastos=total_gastos,
        ganancia_neta=ganancia_neta,
    )
