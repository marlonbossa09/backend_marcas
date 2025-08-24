from models.user_models import User
from models.schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from auth.auth_utils import hash_password, verify_password, create_access_token
from fastapi import HTTPException

def create_user(db: Session, user_data: UserCreate):
    hashed = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        hashed_password=hashed,
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        correo=user_data.correo,
        celular=user_data.celular
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if not user:
        return None
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


def editar_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = user_data.dict(exclude_unset=True)

    if "correo" in update_data:
        correo_existente = (
            db.query(User)
            .filter(User.correo == update_data["correo"], User.id != user_id)
            .first()
        )
        if correo_existente:
            raise HTTPException(status_code=400, detail="El correo ya está en uso por otro usuario.")

    if "username" in update_data:
        username_existente = (
            db.query(User)
            .filter(User.username == update_data["username"], User.id != user_id)
            .first()
        )
        if username_existente:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso por otro usuario.")

    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
