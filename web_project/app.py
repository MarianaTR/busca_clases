from flask import Flask, render_template, request, redirect, url_for,session
from modols.opensearch import search_query, add_document, search, delete_all
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from modols.convert_to_class import convert_to_object
import pandas as pd
#from Models.user import users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Clase.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

class Clase(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text())

    def __init__(self, user_id, name, description):
        self.user_id = user_id
        self.name = name
        self.description = description


@app.route('/', methods=["POST","GET"])
def index():
    #delete_all()
    if request.method == "POST":
        print("hola")
        busqueda = request.form["search"]
        res = search_query(busqueda)
        if res['hits']['hits']:
            value = convert_to_object(res['hits']['hits'])
        else:
            res = search()
            value = convert_to_object(res['hits']['hits'])
        return render_template("index.html", values=value)
    else:
        res = search()
        value = convert_to_object(res['hits']['hits'])
        return render_template("index.html", values=value)

@app.route('/busqueda', methods=["POST","GET"])
def hello_world():  # put application's code here
    print("aqui")




@app.route('/profile/<usr>&<usr_id>')
def profile(usr, usr_id):
    return render_template("profile.html", usr = usr, usr_id=usr_id)

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        user_name = request.form["user"]
        email = request.form["email"]
        password = request.form['password']
        db.create_all()
        user = users(user_name,email,password)
        print("aca")
        db.session.add(user)
        print("aca o99")
        db.session.commit()
        print("pasee")
        user_id = users.query.filter_by(name=user_name).first()
        user_id= user_id._id
        print(user_id)
        clase = Clase(user_id,"futbol","asddnksdfhhs sdfksdhfuhs sdfhsdhfuh")
        print(clase)
        db.session.add(clase)
        db.session.commit()
        add_document(user_id,"futbol","asjdhlass sdifhsudhf")
        print(Clase.query.filter_by(name="pilate").first())
        """
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            pass
        else:
        """
        return redirect(url_for("profile", usr=user_name, usr_id=user_id))
    else:
        return render_template("login.html")

@app.route('/admin')
def admin():
    return render_template("view.html", values=Clase.query.all())

@app.route('/create_class/<user>', methods=['POST','GET'])
def create_clases(user):
    if request.method == "POST":
        name = request.form["user"]
        description = request.form["description"]
        user_id = user
        clase = Clase(user_id, name, description)
        db.session.add(clase)
        db.session.commit()
        add_document(user_id, name, description)
        return redirect(url_for("index"))
    else:
        return  render_template("create_clase.html")

"""@app.route("/<usr>")
def otro(usr):
    return f"<h1>{usr}</h1>"""
if __name__ == '__main__':
    db.create_all()
    app.run()
