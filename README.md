# Passwords-Secure-Vault
[![CI](https://github.com/Javi-kl/Passwords-Secure-Vault/actions/workflows/ci.yml/badge.svg)](https://github.com/Javi-kl/Passwords-Secure-Vault/actions)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
> Backend de un gestor de contraseñas con autenticación JWT y cifrado de bóveda.

> Proyecto enfocado en seguridad y buenas prácticas con FastAPI.

> Documentación: [`architecture.md`](./docs/architecture.md) · [`requisitos.md`](./docs/requisitos.md) · [`esqueleto.md`](./docs/esqueleto.md)
---
## Stack
| Categoría | Tecnología |
|-----------|-----------|
| Framework | FastAPI / Python 3.12+ |
| Base de datos | PostgreSQL 16 + SQLAlchemy 2.0 (sync) |
| Hash de contraseña | Argon2id |
| Cifrado de bóveda | Fernet |
| Derivación de clave | Argon2id raw → Fernet key |
| Sesiones | JWT (PyJWT) · 15 min · cookie httpOnly |
| Validación de contraseña | Longitud mínima 14 + zxcvbn (score ≥ 2) |
| Rate limiting | slowapi |
| Migraciones | Alembic |
| Tests | pytest |
---
## Decisiones de Seguridad
- **Longitud mínima 14 + zxcvbn score ≥ 2.** La longitud es la primera defensa; zxcvbn analiza entropía real detectando secuencias, repeticiones y patrones de teclado.
- **Sin recuperación de contraseña maestra.** La contraseña es el único material de derivación de la clave de cifrado. Sin ella, los datos son irrecuperables.
- **SECRET_KEY validada al arrancar** (mínimo 32 caracteres). Si falta o es corta, la app no arranca.
- **Mensajes de error genéricos en login.** No se revela si el fallo fue por email inexistente o contraseña incorrecta.
- **Sin reglas de composición** (mayúsculas, números, símbolos). OWASP desaconseja forzarlas: reducen la entropía real al incentivar patrones predecibles.
---
## Desarrollo Local
### Prerrequisitos
- Python 3.12+
- Docker y Docker Compose
### Instalación
```bash
git clone https://github.com/Javi-kl/Passwords-Secure-Vault
cd Passwords-Secure-Vault
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # editar con valores locales
```
### Base de datos
> El script de init crea vault_db y vault_test_db automáticamente.
```
chmod +x scripts/init-db.sh
docker compose up -d
```
> Si ya tenías el contenedor levantado antes del script:
```
docker compose down -v    # borra volúmenes (cuidado: pierde datos)
docker compose up -d       # recrea con init-db.sh
```
### Ejecutar la app
```
fastapi dev
```
> Docs interactivas en http://localhost:8000/docs

### Ejecutar tests
```
pytest
```

> 46 tests que cubren login, registro, CRUD, cifrado, ownership, rate limiting, y re-encriptación.

> Los tests usan vault_test_db (definida en TEST_DATABASE_URL del .env), separada de la BD de desarrollo.
 
---
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
- [X] Migraciones con Alembic
- [X] CI con GitHub Actions
- [X] CORS configurado
---
