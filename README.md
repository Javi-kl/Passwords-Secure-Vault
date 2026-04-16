# Passwords-Secure-Vault - Gestor de Contraseñas Backend

Backend de un gestor de contraseñas con autenticación JWT y cifrado de bóveda.

> ⚠️ **Proyecto en desarrollo activo.** La estructura base está definida; la implementación está en curso.

La arquitectura, modelo de datos y requisitos completos están en [`/docs`](./docs).

***

## Stack Tecnológico

- **FastAPI** / Python 3.12+
- **PostgreSQL** + SQLAlchemy 2.0
- **Argon2id** — hash de contraseña maestra
- **Fernet / AES** — cifrado de entradas de bóveda
- **JWT** (PyJWT) — sesiones de 15 minutos
- **Pydantic v2** — validación de schemas
- **Alembic** — migraciones *(pendiente)*
- **pytest** — tests *(pendiente)*

***

## Desarrollo Local

```bash
git clone https://github.com/Javi-kl/Passwords-Secure-Vault
cd Passwords-Secure-Vault

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # completar con valores locales
fastapi dev
```

Docs interactivas en `http://localhost:8000/docs`.

***

## Roadmap

### Autenticación

- [ ] RF1 — Registro con email y contraseña maestra
- [ ] RF2 — Login con JWT (15 min)
- [ ] RF3 — Logout
- [ ] RNF1 — Hash Argon2id (nunca texto plano)
- [ ] RNF4 — Mensajes de error genéricos en login
- [ ] RNF6 — Throttling tras intentos fallidos + logging

### Bóveda

- [ ] RF4 — Crear entrada cifrada
- [ ] RF5 — Listar entradas propias
- [ ] RF6 — Editar entrada propia
- [ ] RF7 — Eliminar entrada propia
- [ ] RNF2 — Cifrado Fernet antes de persistir
- [ ] RNF5 — Control de acceso por propietario (`user_id` del token)

### Infraestructura

- [ ] Migraciones con Alembic
- [ ] Tests con pytest
- [ ] Docker Compose (API + PostgreSQL)
- [ ] Despliegue bajo HTTPS/TLS

***

## Notas

Proyecto de práctica backend enfocado en seguridad (cifrado, autenticación, control de acceso) y arquitectura en capas con FastAPI. No incluye recuperación de contraseña maestra por decisión de diseño.