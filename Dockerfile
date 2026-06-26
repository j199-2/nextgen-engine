FROM python:3.10-slim

# Instalar FFmpeg y dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar archivos de requisitos e instalar
COPY requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt

COPY . .

# Comando seguro que arranca la aplicación sin importar si se llama app.py o aplicación.py
CMD ["sh", "-c", "uvicorn $(ls | grep -E '^(app|aplicación|aplicacion)\.py$' | sed 's/\.py//'):app --host 0.0.0.0 --port 7860"]
