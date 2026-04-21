# Passwords-Secure-Vault
Backend de un gestor de contraseñas con autenticación JWT y cifrado de bóveda.
> Proyecto  enfocado en seguridad (cifrado, autenticación, control de acceso) y buenas prácticas con FastAPI. No incluye recuperación de contraseña maestra ni refresh tokens por decisión de diseño.
La arquitectura, modelo de datos, esqueleto y requisitos completos están en [`/docs`](./docs).
***
## Stack Tecnológico
- **FastAPI** / Python 3.12+
- **PostgreSQL** + SQLAlchemy 2.0 (sync)
- **Argon2id** — hash de contraseña maestra
- **Fernet / AES** — cifrado de entradas de bóveda
- **JWT (PyJWT)** — sesiones de 15 minutos
- **Pydantic v2** — validación de schemas
- **pytest** — tests
***
## Desarrollo Local
### Prerrequisitos
- Python 3.12+
- Docker y Docker Compose
### Instalación
```
git clone https://github.com/Javi-kl/Passwords-Secure-Vault
cd Passwords-Secure-Vault
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
Copiar variables de entorno:
`cp .env.example .env    # completar con valores locales`
Consulta .env.example para ver las variables necesarias.
```
***
### Base de datos
```
Dar permisos de ejecución al script de inicialización:
chmod +x scripts/init-db.sh
Levantar PostgreSQL (crea vault_db y vault_test_db automáticamente):
docker compose up -d
Verificar que ambas BDs existen:
docker compose exec db psql -U vault_user -c "\l"
Si ya tenías el contenedor levantado antes del script de init:
docker compose down -v    # borra volúmenes (cuidado: pierde datos)
docker compose up -d       # recrea con init-db.sh
```
### Ejecutar la app
```
fastapi dev
Docs interactivas en http://localhost:8000/docs.
```
### Ejecutar tests
```
pytest
Los tests usan vault_test_db (definida en TEST_DATABASE_URL del .env), separada de la BD de desarrollo.
```
***
## Roadmap
### Autenticación
- [X] RF1 — Registro con email y contraseña maestra
- [X] RF2 — Login con JWT (10 min) - caducidad forzada de sesión.
- [X] RF3 — Logout
- [X] RNF1 — Hash Argon2id (nunca texto plano)
- [X] RNF4 — Mensajes de error genéricos en login
- [X] RNF6 - Rate limit en registro y login con logs de intentos fallidos, exitos y bloqueos.
### Bóveda
- [ ] RF4 — Crear entrada cifrada
- [ ] RF5 — Listar entradas propias
- [ ] RF6 — Editar entrada propia
- [ ] RF7 — Eliminar entrada propia
- [ ] RNF2 — Cifrado Fernet antes de persistir
- [ ] RNF5 — Control de acceso por propietario (user_id del token)
### Infraestructura
- [ ] Migraciones con Alembic
- [ ] Despliegue bajo HTTPS/TLS