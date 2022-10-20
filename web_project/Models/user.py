from app import db

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    universidad = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    direcc = db.Column(db.String(100))
    clases = db.relationship('Clase')

    def __init__(self, name, email, password, phone, uni, cargo, dire):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.universidad = uni
        self.cargo = cargo
        self.direcc = dire


def get_all_users():
    return users.query.all()