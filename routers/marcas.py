from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.marca import Marca
from models.schemas import MarcaCreate, MarcaUpdate, MarcaOut
from auth.auth_dependencies import get_current_user
from models.user_models import User

router = APIRouter(
    prefix="/servicios/marcas",
    tags=["Marcas"],
    responses={404: {"description": "No encontrado"}},
)
# Crear una nueva marca
@router.post("/",
    response_model=MarcaOut,
    summary="Crear una nueva marca",
    description="Para realizar un servicio de registro de marca, digite los datos requeridos"
)
def create_marca(marca: MarcaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validación duplicados (nombre + titular)
    db_marca_existente = db.query(Marca).filter(
        Marca.nombre == marca.nombre,
        Marca.titular == marca.titular
    ).first()

    if db_marca_existente:
        raise HTTPException(status_code=400, detail="La marca ya está registrada")

    # Si no existe, se crea la nueva marca
    db_marca = Marca(**marca.dict())
    db.add(db_marca)

    try:
        db.commit()
        db.refresh(db_marca)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar la marca")

    return db_marca

# Obtener todas las marcas
@router.get("/",
    response_model=list[MarcaOut],
    summary="Listar todas las marcas",
    description="Obtenga una lista de todas las marcas registradas.")
def list_marcas(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Marca).all()


# Obtener una marca por id
@router.get("/{marca_id}",
    response_model=MarcaOut,
    summary="Obtener una marca por ID",
    description="Devuelve el detalle de una marca específica mediante su ID.")
def get_marca(marca_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca


# Actualizar una marca
@router.put("/{marca_id}",
    response_model=MarcaOut,
    summary="Actualizar una marca",
    description="Modifique los datos de una marca existente mediante su ID.")
def update_marca(marca_id: int, marca: MarcaUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    for key, value in marca.dict(exclude_unset=True).items():
        setattr(db_marca, key, value)

    db.commit()
    db.refresh(db_marca)
    return db_marca

# Eliminar una marca
@router.delete("/{marca_id}",
    summary="Eliminar una marca",
    description="Elimina una marca específica usando su ID.")
def delete_marca(marca_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    db.delete(db_marca)
    db.commit()
    return {"detail": "Marca eliminada correctamente"}