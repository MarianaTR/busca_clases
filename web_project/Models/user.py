from app import db

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    #clases = db.relationship('Clase')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


def get_all_users():
    return users.query.all()