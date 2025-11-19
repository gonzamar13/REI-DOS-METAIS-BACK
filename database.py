import os  # <--- 1. Necesario para leer variables del sistema
from dotenv import load_dotenv # <--- 2. Necesario para cargar el archivo .env
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carga las variables del archivo .env
load_dotenv()

# Obtenemos la URL desde la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL") # <--- 3. Así se obtiene el valor real

# Verificación de seguridad (opcional pero recomendada)
if not DATABASE_URL:
    raise ValueError("No se encontró la variable DATABASE_URL en el archivo .env")

# Creamos el motor usando la variable, NO el texto
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
