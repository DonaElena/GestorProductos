from sqlalchemy import Column, Integer, String, Float, Boolean, Enum
from db import Base
import enum

class CategoriaEnum(enum.Enum):
    hogar = "hogar"
    electronica = "electrónica"
    alimentacion = "alimentación"
    papeleria = "papelería"
    farmacia = "farmacia"
    drogueria = "droguería"

class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    en_stock = Column(Boolean, default=True)
    categoria = Column(Enum(CategoriaEnum), nullable=False)

    def __str__(self):
        return (f"<Producto(nombre='{self.nombre}', precio={self.precio}, "
                f"en_stock={self.en_stock}, categoria='{self.categoria.value}')>")
