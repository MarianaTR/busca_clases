from utils.db import base, engine
from sqlalchemy import Column, Integer, String, ForeignKey


class Clase(base):
    __tablename__ = 'clase'
    _id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100))
    description = Column(String(800))
    duracion = Column(String(20))
    precio = Column(String(20))
    modalidad = Column(String(30))

    def __init__(self, user_id, name, description, duracion, precio, modalidad):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.duracion = duracion
        self.precio = precio
        self.modalidad = modalidad

class users(base):
    __tablename__ = 'users'
    _id = Column("id", Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
    password = Column(String(100))
    phone = Column(String(100))
    universidad = Column(String(100))
    cargo = Column(String(100))
    direcc = Column(String(100))
    clases = ForeignKey("clase")

    def __init__(self, name, email, password, phone, uni, cargo, dire):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.universidad = uni
        self.cargo = cargo
        self.direcc = dire

base.metadata.create_all(engine)

def get_all_users():
    return users.query.all()
