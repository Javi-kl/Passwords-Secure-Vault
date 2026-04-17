## Esqueleto
	```
    PasswordsSecureVault/
├── app/
│   ├── __init__.py                 # Paquete Python vacío
│   ├── main.py                     # Crea la app, registra routers, crea tablas al arrancar
│   ├── dependencies.py             # Dependencias compartidas (get_current_user, etc.) — pendiente
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Settings con pydantic-settings (lee .env)
│   │   └── security.py             # Hash Argon2id, JWT, cifrado Fernet — JWT y Fernet pendientes
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py             # Engine, SessionLocal, Base, get_db (sync)
│   │   └── models/
│   │       ├── __init__.py
│   │       └── user_model.py       # Tabla SQLAlchemy User
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── auth_schema.py          # UserCreate, UserResponse (Pydantic)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── auth_router.py          # POST /auth/register — faltan /login y /logout
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py         # Lógica de registro — falta login y logout
│   └── repositories/
│       ├── __init__.py
│       └── user_repository.py       # find_by_email, create
├── scripts/
│   └── init-db.sh                  # Crea vault_test_db en PostgreSQL 
├── tests/
│   ├── conftest.py                 # Fixtures: TestClient, BD de test, dependency_overrides
│   └── test_auth.py                # Tests del registro (5 tests)
├── docs/
│   ├── esqueleto.md
│   ├── architecture.md             
│   └── requisitos.md               # Requisitos funcionales y no funcionales
├── .env.example                    # ⚠️ Formato incorrecto — necesita valores de ejemplo
├── .gitignore
├── docker-compose.yml             
├── requirements.txt                # ⚠️ Falta pyjwt,
└── README.md                       # ⚠️ Desactualizado — tiene el roadmap viejo
	```
---