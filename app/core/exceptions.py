from fastapi import HTTPException, status


def unauthorized(detail: str = "Credenciales no válidas") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
