from sqlalchemy import Column, Integer, String, UniqueConstraint
from database.db import Base

#Modelo de la tabla
class Marca(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    titular = Column(String, nullable=False)
    estado = Column(String, default="Activo")
    
    
    __table_args__ = (UniqueConstraint("nombre", "titular", name="uq_nombre_titular"),)
