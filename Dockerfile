# =============================================================================
# IMAGEN BASE
# =============================================================================
FROM python:3.12-slim-bookworm

# =============================================================================
# DEPENDENCIAS DEL SISTEMA
# =============================================================================
# libffi-dev y gcc: necesarios para compilar cryptography y argon2
# pkg-config: necesario para encontrar librerías del sistema
# --no-install-recommends: no instala paquetes sugeridos (reduce tamaño)
# rm -rf /var/lib/apt/lists/: limpia cache de apt después de instalar
RUN apt-get update && apt-get install -y \
        gcc \
        libffi-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

# =============================================================================
# DIRECTORIO DE TRABAJO
# =============================================================================
WORKDIR /app

# =============================================================================
# DEPENDENCIAS PYTHON
# =============================================================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# CÓDIGO FUENTE
# =============================================================================
COPY . .


# Directorio para el cache de sesiones vault (diskcache)
RUN mkdir -p /app/tmp_vault_sessions && \
    chmod +x /app/scripts/entrypoint.sh 

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]