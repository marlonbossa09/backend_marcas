from sqlalchemy import Column, Integer, String
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # para login el username
    hashed_password = Column(String)                    # login    
    nombre = Column(String)
    apellido = Column(String)
    correo = Column(String, unique=True, index=True)
    celular = Column(String)