# Usar Python 3.12
FROM python:3.12-slim

# Instalar dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    libgconf-2-4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libnspr4 \
    libnss3 \
    && rm -rf /var/lib/apt/lists/*

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Actualizar pip a la última versión
RUN python -m pip install --upgrade pip

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright y sus navegadores
RUN pip install playwright && \
    playwright install chromium && \
    playwright install-deps

# Copiar el código fuente
COPY . .

# Comando por defecto
CMD ["python", "src/index.py"]