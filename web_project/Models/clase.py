from app import db

class Clase(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text())

    def __init__(self, user_id, name, description):
        self.user_id = user_id
        self.name = name
        self.description = description