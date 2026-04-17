## Esqueleto
	```
    PasswordsSecureVault/
├── app/
│   ├── main.py                     # Crea la app, registra routers, crea tablas al arrancar
│   ├── dependencies.py             # Dependencias compartidas (get_current_user, etc.) — pendiente
│   ├── core/
│   │   ├── config.py               # Settings con pydantic-settings (lee .env)
│   │   └── security.py             # Hash Argon2id, JWT, cifrado Fernet — JWT y Fernet pendientes
│   ├── db/
│   │   ├── database.py             # Engine, SessionLocal, Base, get_db (sync)
│   │   └── models/
│   │       └── user_model.py       # Tabla SQLAlchemy User
│   ├── schemas/
│   │   └── auth_schema.py          # UserCreate, UserResponse (Pydantic)
│   ├── routers/
│   │   └── auth_router.py          # POST /auth/register — faltan /login y /logout
│   ├── services/
│   │   └── auth_service.py         # Lógica de registro — falta login y logout
│   └── repositories/
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
├── .env.example                    
├── .gitignore
├── docker-compose.yml             
├── requirements.txt                
└── README.md                       
	```
---