- ## ARQUITECTURA
	- ## Objetivo
	  Backend de un gestor de contraseñas con FastAPI.
	- ## Alcance MVP
	  Registro, login, logout, cambiar contraseña, CRUD de entradas propias cifradas.
	  No incluye: recuperación de contraseña maestra, compartir contraseñas.
	- ## Capas
		```
		Cliente → Router → Dependencies → Service → Repository → BD
		                                ↓
		                          Security / Crypto
		```
		- **Router**: Endpoints HTTP, validación Pydantic, inyección de dependencies.
		- **Dependencies**: Pre-condiciones compartidas (auth, sesión de bóveda, ownership).
		- **Service**: Lógica de negocio (cifrado, validaciones, errores HTTP).
		- **Repository**: Acceso a BD (SQLAlchemy ORM). Sin lógica de negocio.
		- **Core**: Funciones puras (hash, cifrado, rate limiting, excepciones).
	- ## Dependencies
		```
		auth_user ─→ get_vault_session ─→ endpoint (create, entries, update)
		    │
		    └─→ get_owned_entry ─→ endpoint (update, delete)
		            │
		            └─→ auth_user (sub-dependency)
		```
		- `auth_user`: JWT desde cookie → decode → carga usuario. Retorna `User`.
		- `get_vault_session`: `vault_session_id` del JWT → Fernet desde diskcache. Retorna `Fernet`.
		- `get_owned_entry`: busca entry por ID, valida existencia (404) y ownership (403). Retorna `VaultEntry`.
	- ## Sessión de bóveda
		1. Login: Fernet key derivada de contraseña maestra + vault_salt (Argon2id).
		2. Clave cacheada en diskcache con un `vault_session_id` aleatorio.
		3. `vault_session_id` incluido en el payload JWT.
		4. Cada request a `/vault/*`: `get_vault_session` recupera la clave del cache.
		5. Cambio de contraseña: re-encripta todas las entradas con la nueva clave.
	- ## Modelo de datos
		- ### users
			- id (PK)
			- email (único, indexado)
			- password_hash (Argon2id)
			- vault_salt (16 bytes, generado al registro)
			- created_at (timestamp UTC)
		- ### vault_entries
			- id (PK)
			- user_id (FK → users.id, CASCADE)
			- description
			- encrypted_password (Fernet ciphertext)
			- created_at (timestamp UTC)
			- updated_at (timestamp UTC, auto-update vía ORM)
	- ## Decisiones técnicas
		- PostgreSQL 16 como BD.
		- JWT en cookie httpOnly (no Authorization header).
		- Fernet (AES-128-CBC + HMAC-SHA256) para cifrado de bóveda.
		- Argon2id para hash de contraseña y derivación de clave.
		- Capas: Router → Dependency → Service → Repository.
		- SQLAlchemy 2.0 (db.get, select, ORM-style mutations).
		- Excepciones HTTP centralizadas en factory (core/exceptions.py).
		- Rate limiting con slowapi (register: 3/min, login: 5/min, password: 1/min).
	- ## Endpoints
		- ### Auth
			- POST /auth/register (3/min)
			- POST /auth/login (5/min)
			- POST /auth/logout
			- GET /auth/me
			- PATCH /auth/password (1/min)
		- ### Vault
			- POST /vault/create
			- GET /vault/entries
			- PATCH /vault/update/{entry_id}
			- DELETE /vault/delete/{entry_id}
	- ## Tests
		- Cobertura: auth (registro, login, logout, middleware, cambio de contraseña) y vault (CRUD completo + cifrado + ownership).
		- Fixtures: client, authed_client, second_authed_client, db, reset_db, reset_limiter.
		- BD de test separada (TEST_DATABASE_URL) con recreate por test (drop_all + create_all).
	- ## Opcionales para producción
		- Alembic para migraciones de esquema.
		- HTTPS obligatorio (reverse proxy).
		- Auditoría de accesos (logging estructurado).
---