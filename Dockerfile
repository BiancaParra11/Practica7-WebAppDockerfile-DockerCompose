FROM python:3.11-slim

WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente desde src hacia el contenedor
COPY src/ .

EXPOSE 5000

CMD ["python", "app.py"]
