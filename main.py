from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import crud, schemas
from typing import List
from fastapi.middleware.cors import CORSMiddleware
    
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema REI DOS METAIS")

# Lista explícita de orígenes permitidos (CORS Correcto)
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://reidosmetais.mindcube.cloud", # Frontend HTTPS
    "http://reidosmetais.mindcube.cloud",  # Frontend HTTP
    "https://back.mindcube.cloud"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CLIENTES ---
@app.post("/clientes/", response_model=schemas.ClienteResponse)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.crear_cliente(db, cliente)

@app.get("/clientes/", response_model=List[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return crud.listar_clientes(db)

@app.get("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    c = crud.obtener_cliente(db, cliente_id)
    if not c: raise HTTPException(404, "Cliente no encontrado")
    return c

@app.put("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    c = crud.actualizar_cliente(db, cliente_id, cliente)
    if not c: raise HTTPException(404, "Cliente no encontrado")
    return c

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    c = crud.eliminar_cliente(db, cliente_id)
    if not c: raise HTTPException(404, "Cliente no encontrado")
    return {"message": "Cliente eliminado"}

# --- PRODUCTOS ---
@app.post("/productos/", response_model=schemas.ProductoResponse)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.crear_producto(db, producto)

@app.get("/productos/", response_model=List[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.listar_productos(db)

@app.get("/productos/{id}", response_model=schemas.ProductoResponse)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    p = crud.obtener_producto(db, id)
    if not p: raise HTTPException(404, "Producto no encontrado")
    return p

@app.put("/productos/{id}", response_model=schemas.ProductoResponse)
def actualizar_producto(id: int, prod: schemas.ProductoCreate, db: Session = Depends(get_db)):
    p = crud.actualizar_producto(db, id, prod)
    if not p: raise HTTPException(404, "Producto no encontrado")
    return p

@app.delete("/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    p = crud.eliminar_producto(db, id)
    if not p: raise HTTPException(404, "Producto no encontrado")
    return {"message": "Producto eliminado"}

# --- VENTAS ---
@app.post("/ventas/", response_model=schemas.VentaResponse)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    return crud.crear_venta(db, venta)

@app.get("/ventas/", response_model=List[schemas.VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    ventas = crud.listar_ventas(db)
    resultado = []
    
    # Transformación manual con protección contra datos nulos (clientes/productos borrados)
    for v in ventas:
        detalles_resp = []
        for d in v.detalles:
            detalles_resp.append({
                # Protección: Si el producto se borró, mostramos "Borrado"
                "producto_nombre": d.producto.nombre if d.producto else "Producto Eliminado",
                "cantidad": d.cantidad,
                "precio_unitario": d.precio_unitario,
                "subtotal": d.subtotal
            })
        
        resultado.append({
            "id": v.id,
            "fecha": v.fecha,
            "total": v.total,
            "forma_de_pago": v.forma_de_pago,
            # Protección: Si el cliente se borró, pasamos None (gracias al cambio en schemas.py)
            "cliente": v.cliente if v.cliente else None,
            "detalles": detalles_resp
        })
    return resultado

@app.delete("/ventas/{id}")
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    v = crud.eliminar_venta(db, id)
    if not v: raise HTTPException(404, "Venta no encontrada")
    return {"message": "Venta eliminada"}