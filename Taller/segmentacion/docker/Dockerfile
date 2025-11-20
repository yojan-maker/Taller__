# Imagen base ligera y estable para YOLO + Streamlit
FROM python:3.11-slim

# Evitar interacción en la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de la app
WORKDIR /app

# Copiar requirements
COPY docker/requirements.txt requirements.txt

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer el puerto del dashboard
EXPOSE 8501

# Comando para ejecutar Streamlit en el contenedor
CMD ["streamlit", "run", "app/dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
