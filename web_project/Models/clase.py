from app import db

class Clase(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text())
    duracion = db.Column(db.String(20))
    precio = db.Column(db.String(20))
    modalidad = db.Column(db.String(30))

    def __init__(self, user_id, name, description, duracion,precio,modalidad):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.duracion = duracion
        self.precio = precio
        self.modalidad = modalidad