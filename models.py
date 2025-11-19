from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False) # [cite: 51]
    correo = Column(String, unique=True)
    # Historial se deriva de la relación ventas

    ventas = relationship("Venta", back_populates="cliente")

class Producto(Base): # Renombrado de Servicio a Producto [cite: 51]
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False) # Puerta, Ventana, etc. [cite: 51]
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0) # [cite: 29, 68]

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now) # 
    total = Column(Float, nullable=False)
    forma_de_pago = Column(String, nullable=False) # Efectivo, Transferencia [cite: 73]

    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="ventas")
    
    # Relación con detalles
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

class DetalleVenta(Base): # Nueva entidad para manejar cantidad [cite: 51]
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False) # Precio al momento de la venta
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")