- ## *Requisitos funcionales*
	- ## RF1. Registro de usuario
		- **Historia:** Como visitante, quiero registrarme con email y contraseña maestra para crear mi cuenta.
		    
		  **Criterios de aceptación:**  
		- DADO que envío email válido y contraseña válida, CUANDO me registro, ENTONCES la cuenta se crea.
		- DADO que el email ya existe, CUANDO intento registrarme, ENTONCES recibo error controlado.
		- DADO que falta un campo o el email es inválido, CUANDO envío el formulario, ENTONCES recibo error de validación.
		- DADO que la contraseña no cumple la política mínima, CUANDO intento registrarme, ENTONCES el sistema rechaza el registro.
		    

	- ## RF2. Login de usuario
		- **Historia:** Como usuario registrado, quiero iniciar sesión con mi email y contraseña maestra para acceder a mi bóveda.
		    
		  **Criterios de aceptación:**  
		- DADO que las credenciales son correctas, CUANDO hago login, ENTONCES recibo un JWT válido durante 15 minutos.
		- DADO que las credenciales son incorrectas, CUANDO hago login, ENTONCES recibo 401 con mensaje genérico.
		- DADO que falta email o contraseña, CUANDO hago login, ENTONCES recibo error de validación.
		- DADO que supero el límite de intentos fallidos, CUANDO vuelvo a intentarlo, ENTONCES el sistema aplica bloqueo temporal o retraso.
		    

	- ## RF3. Logout de usuario
		- **Historia:** Como usuario autenticado, quiero cerrar sesión para dejar de usar la aplicación de forma segura.
		    
		  **Criterios de aceptación:**  
		- DADO que estoy autenticado, CUANDO hago logout, ENTONCES el cliente elimina el token.
		- DADO que intento acceder con un token ausente o expirado, CUANDO llamo a un endpoint protegido, ENTONCES recibo 401.

	- ## RF4. Crear entrada de bóveda
		- **Historia:** Como usuario autenticado, quiero guardar una contraseña con una descripción para almacenarla en mi bóveda.
		    
		  **Criterios de aceptación:**  
		- DADO que estoy autenticado, CUANDO creo una entrada válida, ENTONCES se guarda asociada a mi usuario.
		- DADO que faltan datos obligatorios, CUANDO intento crear la entrada, ENTONCES recibo error de validación.
		- DADO que la entrada se guarda, CUANDO se persiste en BD, ENTONCES la contraseña queda cifrada y no en texto plano.
		    

	- ## RF5. Listar mis entradas
		- **Historia:** Como usuario autenticado, quiero ver mis entradas para consultar mi bóveda.
		    
		  **Criterios de aceptación:**  
		- DADO que tengo entradas, CUANDO consulto el listado, ENTONCES solo veo las mías.
		- DADO que no tengo entradas, CUANDO consulto el listado, ENTONCES recibo lista vacía.
		- DADO que no estoy autenticado, CUANDO consulto el listado, ENTONCES recibo 401.
		    

	- ## RF6. Editar una entrada propia
		- **Historia:** Como usuario autenticado, quiero editar una entrada de mi bóveda para mantenerla actualizada.
		    
		  **Criterios de aceptación:**  
		- DADO que la entrada existe y es mía, CUANDO envío cambios válidos, ENTONCES la entrada se actualiza.
		- DADO que la entrada no existe, CUANDO intento editarla, ENTONCES recibo 404.
		- DADO que la entrada no es mía, CUANDO intento editarla, ENTONCES la operación se rechaza.
		    

	- ## RF7. Eliminar una entrada propia
		- **Historia:** Como usuario autenticado, quiero borrar una entrada de mi bóveda.
		    
		  **Criterios de aceptación:**  
		- DADO que la entrada existe y es mía, CUANDO la elimino, ENTONCES se borra correctamente.
		- DADO que la entrada no existe, CUANDO intento borrarla, ENTONCES recibo 404.
		- DADO que la entrada no es mía, CUANDO intento borrarla, ENTONCES la operación se rechaza.
	
	- ## RF8. Cambiar contraseña maestra
		- **Historia:** Como usuario autenticado, quiero cambiar mi contraseña maestra para mantener la seguridad de mi cuenta.
		    
		  **Criterios de aceptación:**  
		- DADO que la contraseña actual es correcta, CUANDO envío una nueva contraseña válida, ENTONCES se actualiza el hash y se re-encriptan todas las entradas de la bóveda con la nueva clave.
		- DADO que la contraseña actual es incorrecta, CUANDO intento cambiarla, ENTONCES recibo 401.
		- DADO que la nueva contraseña es igual a la actual, CUANDO intento cambiarla, ENTONCES recibo 400.
		- DADO que la nueva contraseña y la confirmación no coinciden, CUANDO intento cambiarla, ENTONCES recibo 422.
		- DADO que la re-encriptación falla, CUANDO se produce un error de cifrado, ENTONCES recibo 500 y las entradas no se modifican (rollback).
		- DADO que el usuario no tiene entradas en la bóveda, CUANDO cambia la contraseña, ENTONCES la operación se completa sin error.
---
- ## *Requisitos no funcionales*
	- ## RNF1. Seguridad de contraseña maestra
		- **Historia:** Como usuario, quiero que mi contraseña maestra no se almacene en claro para proteger mi cuenta.
		    
		  **Criterios de aceptación:**  
		- La contraseña maestra nunca se guarda en texto plano.
		- Solo se almacena un hash adaptativo con sal única por usuario (Argon2id).
		- La validación de fortaleza usa zxcvbn (score mínimo 2) según OWASP.
		- No se imponen reglas de composición.
		    

	- ## RNF2. Cifrado de contraseñas de la bóveda
		- **Historia:** Como usuario, quiero que las contraseñas guardadas estén cifradas para proteger mis datos.
		    
		  **Criterios de aceptación:**  
		- Ninguna contraseña de la bóveda se guarda en texto plano.
		- El backend cifra la contraseña antes de persistirla.
		- El diseño usa una clave derivada de la contraseña maestra, según tu enfoque actual.
		    

	- ## RNF3. Autenticación y sesión
		- **Historia:** Como usuario, quiero que mi sesión tenga una duración corta para reducir riesgo si el token se filtra.
		    
		  **Criterios de aceptación:**  
		- El acceso autenticado usa JWT con expiración de 15 minutos.
		- Todo endpoint protegido exige token válido.
		- Un token expirado devuelve 401.
		    

	- ## RNF4. Privacidad en login
		- **Historia:** Como usuario, quiero que el sistema no revele datos sensibles en los errores de acceso.
		    
		  **Criterios de aceptación:**  
		- Los errores de login usan mensaje genérico.
		- El sistema no indica si el fallo es por email inexistente o contraseña incorrecta.
		    

	- ## RNF5. Control de acceso por propietario
		- **Historia:** Como usuario, quiero que nadie pueda acceder a mis entradas.
		    
		  **Criterios de aceptación:**  
		- Cada entrada pertenece a un único usuario.
		- El `user_id` se toma del token, no del body enviado por el cliente.
		- Un usuario no puede leer, editar ni borrar entradas ajenas.
		    

	- ## RNF6. Protección básica ante ataques
		- **Historia:** Como propietario del sistema, quiero limitar las peticiones de autenticación y registro.
		registrar los intentos fallidos para mitigar ataques de fuerza bruta.
		    
		  **Criterios de aceptación:**
		- El endpoint POST /auth/login aplica rate limiting de 5 peticiones
			por minuto por IP.
		- El endpoint POST /auth/register aplica rate limiting de 3 peticiones
			por minuto por IP.
		- Cuando se supera el límite, se devuelve HTTP 429 con mensaje
			descriptivo.
		- Cada intento de login fallido se registra en logs con nivel WARNING,
			incluyendo el email intentado, sin distinguir si falló por email
			inexistente o contraseña incorrecta (consistente con RNF4).
		- Cada intento de login exitoso se registra en logs con nivel INFO.
		- Cada superación de rate limit se registra en logs con nivel WARNING,
			incluyendo la IP y el path.
		    

	- ## RNF7. Transporte seguro
		- **Historia:** Como usuario, quiero que mis credenciales viajen cifradas para evitar exposición.
		    
		  **Criterios de aceptación:**  
		- La aplicación se usa bajo HTTPS/TLS en despliegue.
		    

	- ## RNF8. Sin recuperación de contraseña maestra
		- **Historia:** Como usuario, quiero saber que la contraseña maestra no se puede recuperar.
		    
		  **Criterios de aceptación:**  
		- El sistema no ofrece recuperación de contraseña maestra.
		- Si el usuario la pierde, pierde acceso a la bóveda.
        