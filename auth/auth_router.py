from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.schemas import UserCreate, UserOut,UserLogin, UserUpdate
from auth.auth_service import create_user, login_user, editar_user
from database.db import SessionLocal
from auth.auth_dependencies import get_current_user
from models.user_models import User

router = APIRouter(tags=["Auth & Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=UserOut, summary="Obtener datos del usuario actual")
def get_current_user_data(current_user: User = Depends(get_current_user)):
    """
    Retorna la información del usuario autenticado usando el token JWT.
    """

    return current_user

@router.put("/me", response_model=UserOut, summary="Actualizar usuario en sesión")
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar los datos del usuario autenticado.
    """
    user = editar_user(db, current_user.id, data)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user



@router.post("/register/", response_model=UserOut, summary="Registrar nuevo usuario")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    """
    return create_user(db, user)

@router.post("/login/", summary="Iniciar sesión y obtener token")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Verifica las credenciales y retorna un **token JWT** válido.
    """
    token = login_user(db, user.username, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return token

