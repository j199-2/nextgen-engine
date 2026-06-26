FROM python:3.10-slim

# Instalar FFmpeg y herramientas del sistema necesarias
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt

COPY . .

CMD ["uvicorn", "aplicación:app", "--host", "0.0.0.0", "--port", "7860"]
