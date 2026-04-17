- ## ARQUITECTURA
	- ## Objetivo
	  Backend de un gestor de contraseñas con FastAPI.  

	- ## Alcance MVP
	  Incluye: registro, login, logout, crear/listar/editar/borrar entradas propias cifradas.  
	  No incluye: recuperación de contraseña maestra, compartir contraseñas.  

	- ## Piezas principales
		- Router
		- Auth dependency
		- Service
		- Repository
		- Security
		- Database

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
		- JWT para autenticación.
		- Fernet/AES para cifrado de la bóveda
		- Argon2id para hash de contraseña maestra
		- Arquitectura en capas simple.
		- SQLAlchemy 2.0 como ORM

	- ## Opcionales para producción
		- alembic
		
	- ## Base de datos de test
		- Un solo servicio PostgreSQL en docker-compose con init script que crea vault_test_db
		- conftest.py usa dependency_overrides para apuntar los tests a TEST_DATABASE_URL
		Por qué: BD de test separada sin duplicar contenedores. Simple para aprender, correcto para producción.
---