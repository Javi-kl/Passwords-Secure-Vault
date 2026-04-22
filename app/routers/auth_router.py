from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.db.database import get_db
from app.db.models.user_model import User
from app.dependencies.auth_deps import auth_user
from app.schemas.auth_schema import MessageResponse, UserCreate, UserResponse,ChangePasswordRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("3/minute")
def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register(user_data, db)


@router.post("/login", response_model=MessageResponse, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def login(
    response: Response,
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return AuthService.login(form, db, response)


@router.post(
    "/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user)]
)
def logout(response: Response):
    return AuthService.logout(response)


@router.patch(
    "/password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("1/minute")
def change_password(
    request: Request,
    password_data: ChangePasswordRequest,
    user: User = Depends(auth_user),
    db: Session = Depends(get_db),
):

    return AuthService.change_password_service(
        user, password_data, db
    )


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(auth_user)):
    return UserResponse.model_validate(user)
