## Esqueleto
	```
    PasswordsSecureVault/
├── app/
│   ├── main.py                         # Crea la app, precarga zxcvbn, registra routers
│   ├── core/
│   │   ├── config.py                   # Settings con pydantic-settings (lee .env)
│   │   ├── exceptions.py               # Factory de excepciones HTTP (unauthorized, etc.)
│   │   ├── logging_config.py           # Configuración de logging
│   │   ├── rate_limit.py               # slowapi limiter 
│   │   ├── security.py                 # Hash Argon2id, verify, validación zxcvbn
│   │   ├── vault_crypto.py             # Derivación de clave Fernet, encrypt/decrypt, re_encrypt
│   │   └── vault_session_cache.py      # Cache de sesiones Fernet con diskcache
│   ├── db/
│   │   ├── database.py                 # Engine, SessionLocal, Base, get_db (sync, commit/rollback)
│   │   └── models/
│   │       ├── user_model.py           # Tabla SQLAlchemy User (email, password_hash, vault_salt)
│   │       └── vault_model.py          # Tabla SQLAlchemy VaultEntry (user_id FK, encrypted_password)
│   ├── dependencies/
│   │   ├── auth_deps.py                # auth_user: extrae JWT de cookie, retorna User
│   │   └── vault_deps.py               # get_vault_session: Fernet desde cache; get_owned_entry: 404+403
│   ├── repositories/
│   │   ├── user_repository.py           # create, get_by_email, get_by_id, update_password (ORM-style)
│   │   └── vault_repository.py          # create, update, delete, get_all_by_user_id, get_by_id (ORM-style)
│   ├── routers/
│   │   ├── auth_router.py               # /auth/* endpoints (register, login, logout, me, password)
│   │   ├── health_router.py             # /health (SELECT 1 para verificar conexión a BD)
│   │   └── vault_router.py              # /vault/* endpoints (create, entries, update, delete)
│   ├── schemas/
│   │   ├── auth_schema.py              # UserCreate, UserResponse, ChangePasswordRequest, MessageResponse
│   │   └── vault_schema.py             # EntryCreate (validación), EntryRead (serialización)
│   └── services/
│       ├── auth_service.py             # register, login, logout, change_password (re-encriptación)
│       └── vault_service.py            # create_entry, get_entries, update_entry, delete_entry
├── scripts/
│   ├── entrypoint.sh                   # Ejecuta migraciones Alembic y arranca uvicorn (Docker)
│   └── init-db.sh                      # Crea vault_test_db en PostgreSQL
├── tests/
│   ├── conftest.py                     # Fixtures: client, authed_client, second_authed_client, db, reset_db
│   ├── tests_auth/
│   │   ├── test_register.py            
│   │   ├── test_login.py               
│   │   ├── test_auth_user.py           
│   │   ├── test_logout.py              
│   │   └── test_change_password.py     
│   └── tests_vault/
│       ├── test_create_entry.py        
│       ├── test_get_entries.py          
│       ├── test_update_entry.py         
│       └── test_delete_entry.py        
├── docs/
│   ├── architecture.md                 
│   ├── esqueleto.md                    
│   └── requisitos.md                   
├── .env.example                        
├── .gitignore
├── docker-compose.yml                  # PostgreSQL + app
├── pyproject.toml                      # Configuración de pytest
├── requirements.txt                    
└── README.md
	```
---