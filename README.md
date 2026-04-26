# Passwords-Secure-Vault
Backend de un gestor de contraseñas con autenticación JWT y cifrado de bóveda.
> Proyecto enfocado en seguridad (cifrado, autenticación, control de acceso) y buenas prácticas con FastAPI. No incluye recuperación de contraseña maestra ni refresh tokens por decisión de diseño.

- [`architecture.md`](./docs/architecture.md) — Capas, dependencies, flujos, decisiones técnicas.
- [`requisitos.md`](./docs/requisitos.md) — Requisitos funcionales y no funcionales.
- [`esqueleto.md`](./docs/esqueleto.md) — Estructura de archivos del proyecto.
***
## Stack Tecnológico
- **FastAPI** / Python 3.12+
- **PostgreSQL** + SQLAlchemy 2.0 (sync)
- **Argon2id** — hash de contraseña maestra y derivación de clave Fernet
- **Fernet** — cifrado de entradas de bóveda
- **JWT (PyJWT)** — sesiones de 15 minutos, cookie httpOnly
- **diskcache** — cache de sesiones de bóveda (claves Fernet)
- **Pydantic v2** — validación de schemas
- **slowapi** — rate limiting
- **pytest** — tests
***
## Desarrollo Local
### Prerrequisitos
- Python 3.12+
- Docker y Docker Compose
### Instalación
git clone https://github.com/Javi-kl/Passwords-Secure-Vault
cd Passwords-Secure-Vault
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # completar con valores locales
### Base de datos
chmod +x scripts/init-db.sh
docker compose up -d
El script de init crea `vault_db` y `vault_test_db` automáticamente.  
Si ya tenías el contenedor levantado antes del script:
docker compose down -v    # borra volúmenes (cuidado: pierde datos)
docker compose up -d       # recrea con init-db.sh
### Ejecutar la app
fastapi dev
Docs interactivas en http://localhost:8000/docs.
### Ejecutar tests
pytest
Los tests usan `vault_test_db` (definida en `TEST_DATABASE_URL` del .env), separada de la BD de desarrollo.
***
## Roadmap
### Autenticación
- [X] RF1 — Registro con email y contraseña maestra
- [X] RF2 — Login con JWT (15 min, cookie httpOnly)
- [X] RF3 — Logout
- [X] RF8 — Cambio de contraseña maestra (re-encriptación de bóveda)
- [X] RNF1 — Hash Argon2id (nunca texto plano)
- [X] RNF4 — Mensajes de error genéricos en login
- [X] RNF6 — Rate limiting (registro 3/min, login 5/min, password 1/min)
### Bóveda
- [X] RF4 — Crear entrada cifrada
- [X] RF5 — Listar entradas propias
- [X] RF6 — Editar entrada propia
- [X] RF7 — Eliminar entrada propia
- [X] RNF2 — Cifrado Fernet antes de persistir
- [X] RNF5 — Control de acceso por propietario (ownership en update/delete)
### Infraestructura
- [ ] Migraciones con Alembic
- [ ] Despliegue bajo HTTPS/TLS