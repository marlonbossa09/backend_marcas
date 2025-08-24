from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from typing import Literal


#Marca Shema
class MarcaBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=30)
    titular: str = Field(..., min_length=3, max_length=30)

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(MarcaBase):
    nombre: Optional[str] = Field(None, min_length=3, max_length=30)
    titular: Optional[str] = Field(None, min_length=3, max_length=30)
    estado: Optional[Literal["Activo", "Inactivo", "Suspendido"]] = None

class MarcaOut(BaseModel):
    id: int
    nombre: str
    titular: str
    estado: str

    class Config:
        from_attributes = True
        
# User schema
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(..., min_length=6, max_length=30)
    nombre: str = Field(..., min_length=3, max_length=20)
    apellido: str = Field(..., min_length=3, max_length=20)
    correo: EmailStr
    celular: str = Field(..., pattern=r'^\+?\d{10,15}$')
    
class UserOut(BaseModel):
    id: int
    username: str
    nombre: str
    apellido: str
    correo: EmailStr
    celular: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=15)
    password: Optional[str] = Field(None, min_length=6, max_length=30)
    nombre: Optional[str] = Field(None, min_length=3, max_length=20)
    apellido: Optional[str] = Field(None, min_length=3, max_length=20)
    correo: Optional[EmailStr] = None
    celular: Optional[str] = Field(None, pattern=r'^\+?\d{10,15}$')

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str