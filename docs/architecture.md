- ## ARQUITECTURA
	- ## Objetivo
	  Backend de un gestor de contraseñas con FastAPI.  

	- ## Alcance MVP
	  Incluye: registro, login, logout, crear/listar/editar/borrar entradas propias cifradas.  
	  No incluye: recuperación de contraseña maestra, compartir contraseñas.  

	- ## Piezas principales
		- Router
		  logseq.order-list-type:: number
		- Auth dependency
		  logseq.order-list-type:: number
		- Service
		  logseq.order-list-type:: number
		- Repository
		  logseq.order-list-type:: number
		- Security
		  logseq.order-list-type:: number
		- Database
		  logseq.order-list-type:: number

	- ## Flujos clave
		- Login: Cliente -> Router -> Service -> Repository -> Security -> Response
		- Crear entrada: Cliente -> Router -> Auth -> Service -> Security -> Repository -> DB -> Response

	- ## Modelo de datos
		- ### users
			- id
			- email
			- password_hash
		- ### vault_entries
			- id
			- user_id
			- description
			- encrypted_password
		-

	- ## Decisiones técnicas
		- PostgreSQL como BD.
		  logseq.order-list-type:: number
		- JWT para autenticación.
		  logseq.order-list-type:: number
		- Fernet/AES para cifrado de la bóveda
		  logseq.order-list-type:: number
		- Argon2id para hash de contraseña maestra
		  logseq.order-list-type:: number
		- Arquitectura en capas simple.
		  logseq.order-list-type:: number
		- SQLAlchemy 2.0 como ORM
		  logseq.order-list-type:: number
	-

	- ## Opcionales para producción
		- alembic


	- ## Esqueleto
	  ```
	PasswordsSecureVault/
	├── app/
	│   ├── main.py
	│   ├── dependencies.py
	│   ├── core/
	│   │   ├── config.py
	│   │   └── security.py
	│   ├── db/
	│   │   ├── database.py
	│   │   └── models/
	│   │       ├── user.py
	│   │       └── vault_entry.py
	│   ├── schemas/
	│   │   ├── auth.py
	│   │   └── vault.py
	│   ├── routers/
	│   │   ├── auth.py
	│   │   └── vault.py
	│   ├── services/
	│   │   ├── auth_service.py
	│   │   └── vault_service.py
	│   └── repositories/
	│       ├── user_repository.py
	│       └── vault_repository.py
	├── alembic/
	├── tests/
	├── docs/
	├── docker-compose.yml
	├── .env.example
	├── .gitignore
	└── README.md
---