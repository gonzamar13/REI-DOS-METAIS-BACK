FROM python:3.10-slim

# Directorio dentro del contenedor
WORKDIR /app

# Copiamos dependencias
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY . .

# Exponemos el puerto
EXPOSE 8001

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
