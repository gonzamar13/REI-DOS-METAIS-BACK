from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Clientes ---
class ClienteBase(BaseModel):
    nombre: str
    telefono: str
    correo: str

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    class Config:
        orm_mode = True

# --- Productos ---
class ProductoBase(BaseModel):
    nombre: str
    tipo: str
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    class Config:
        orm_mode = True

# --- Ventas ---
class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int

class DetalleVentaResponse(BaseModel):
    producto_nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class VentaCreate(BaseModel):
    cliente_id: int
    forma_de_pago: str
    detalles: List[DetalleVentaCreate]

class VentaResponse(BaseModel):
    id: int
    fecha: datetime
    total: float
    forma_de_pago: str
    cliente: ClienteResponse
    detalles: List[DetalleVentaResponse] # Detalle anidado

    class Config:
        orm_mode = True