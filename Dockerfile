FROM python:3.13-slim

# Install system deps (если надо: gcc, libffi, ... — но здесь не нужны)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for Docker cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (исключая лишнее через .dockerignore)
COPY . .

# Гарантируем папку для БД
RUN mkdir -p /app/data

# main entry
CMD ["python", "main.py"]
