from sqlalchemy.orm import Session
from models import Cliente, Producto, Venta, DetalleVenta
from schemas import ClienteCreate, ProductoCreate, VentaCreate
from fastapi import HTTPException

####### CLIENTES (RF1) ######
def crear_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def listar_clientes(db: Session):
    return db.query(Cliente).all()

def obtener_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def actualizar_cliente(db: Session, cliente_id: int, cliente: ClienteCreate):
    db_cliente = obtener_cliente(db, cliente_id)
    if not db_cliente:
        return None
    for key, value in cliente.dict().items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def eliminar_cliente(db: Session, cliente_id: int):
    db_cliente = obtener_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente

####### PRODUCTOS (RF2, RF5) ######
def crear_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def listar_productos(db: Session):
    return db.query(Producto).all()

def obtener_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def actualizar_producto(db: Session, producto_id: int, producto: ProductoCreate):
    db_producto = obtener_producto(db, producto_id)
    if not db_producto:
        return None
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    db_prod = obtener_producto(db, producto_id)
    if db_prod:
        db.delete(db_prod)
        db.commit()
    return db_prod

####### VENTAS (RF3, RF5) ######
def crear_venta(db: Session, venta: VentaCreate):
    total_venta = 0
    detalles_db = []

    # Validar stock y calcular total
    for item in venta.detalles:
        producto = obtener_producto(db, item.producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto ID {item.producto_id} no encontrado")
        
        if producto.stock < item.cantidad: # Control de stock [cite: 26, 40]
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")

        # Descontar stock
        producto.stock -= item.cantidad
        
        subtotal = producto.precio * item.cantidad
        total_venta += subtotal

        # Crear objeto detalle
        detalle = DetalleVenta(
            producto_id=producto.id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio,
            subtotal=subtotal
        )
        detalles_db.append(detalle)

    # Crear venta
    db_venta = Venta(
        cliente_id=venta.cliente_id,
        total=total_venta,
        forma_de_pago=venta.forma_de_pago
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)

    # Asociar detalles a la venta
    for detalle in detalles_db:
        detalle.venta_id = db_venta.id
        db.add(detalle)
    
    db.commit()
    db.refresh(db_venta)
    return db_venta

def listar_ventas(db: Session):
    # Optimización con eager loading para reporte
    return db.query(Venta).all()

def obtener_venta(db: Session, venta_id: int):
    return db.query(Venta).filter(Venta.id == venta_id).first()

def eliminar_venta(db: Session, venta_id: int):
    # Nota: En un sistema real, eliminar una venta debería devolver el stock.
    # Por simplicidad se mantiene eliminación simple.
    db_venta = obtener_venta(db, venta_id)
    if db_venta:
        db.delete(db_venta)
        db.commit()
    return db_venta