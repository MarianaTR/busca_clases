from flask import Flask, render_template, request, redirect, url_for,session
from modols.opensearch import search_query, add_document, search, delete_all
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from modols.convert_to_class import convert_to_object
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
import requests
import pandas as pd
#from Models.user import users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Clase.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
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

@app.route('/ping')
def do_ping():
    ping = 'Ping ...'

    response = ''
    try:
        response = requests.get('http://opensearch_node1:9200/iaps-index/_search')
        print(response.text)
    except requests.exceptions.RequestException as e:
        print('\n Cannot reach the pong service.')
        return 'Ping ...\n'

    return 'Ping ... '+ response.text+ ' '+ str(type(response))+' \n'
@app.route('/', methods=["POST","GET"])
def index():
    #delete_all()
    if request.method == "POST":
        busqueda = request.form["search"]
        res = search_query(busqueda)
        if res['hits']['hits']:
            value = convert_to_object(res['hits']['hits'])
        else:
            #res = search()
            value = convert_to_object(res['hits']['hits'])
        return render_template("index.html", values=value)
    else:
        res = search()
        value = convert_to_object(res['hits']['hits'])
        return render_template("index.html", values=value)

@app.route('/busqueda', methods=["POST","GET"])
def hello_world():  # put application's code here
    print("aqui")




@app.route('/profile/<usr>')
def profile(usr):
    usr = users.query.filter_by(_id = usr).first()
    return render_template("profile.html", usr = usr)

@app.route('/signin', methods=["POST","GET"])
def signin():
    #db.session.execute(f'DROP TABLE Clase')
    db.create_all()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form['password']
        user = users.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                return render_template("profile.html", usr=user)
            else:
                return redirect(url_for("signin"))
        else:
            return redirect(url_for("signin"))
    else:
        return render_template("signin.html")

@app.route('/login', methods=["POST","GET"])
def login():
    engine = create_engine('sqlite://', echo=False)
    #db.session.execute(f'DROP TABLE users')
    db.create_all()
    if request.method == "POST":
        user_name = request.form["user"]
        email = request.form["email"]
        password = request.form['password']
        universidad = request.form['uni']
        phone = request.form['phone']
        cargo = request.form['cargo']
        direc = request.form['dir']
        user = users(user_name,email,password,phone,universidad,cargo,direc)
        db.session.add(user)
        user_id = users.query.filter_by(name=user_name).first()
        user_id = user_id._id
        try:
            db.session.commit()
            """print("pasee")
            user_id = users.query.filter_by(name=user_name).first()
            user_id= user_id._id
            print(user_id)
            clase = Clase(user_id,"futbol","asddnksdfhhs sdfksdhfuhs sdfhsdhfuh")
            print(clase)
            db.session.add(clase)
            db.session.commit()
            add_document(user_id,"futbol","asjdhlass sdifhsudhf")
            print(Clase.query.filter_by(name="pilate").first())"""
        except:
            return render_template("login.html")

            db.session.rollback()
        """
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            pass
        else:
        """
        return redirect(url_for("profile", usr=user_id))
    else:
        return render_template("login.html")

@app.route('/admin')
def admin():
    return render_template("view.html", values=Clase.query.all())

@app.route('/create_class/<user>', methods=['POST','GET'])
def create_clases(user):
    db.create_all()
    if request.method == "POST":
        name = request.form["user"]
        description = request.form["description"]
        duracion = request.form['duracion']
        precio = request.form['precio']
        modalidad = request.form['modalidad']
        user_id = user
        clase = Clase(user_id, name, description,duracion,precio,modalidad)
        db.session.add(clase)
        db.session.commit()
        add_document(user_id, clase)
        return redirect(url_for("index"))
    else:
        return  render_template("create_clase.html")

"""@app.route("/<usr>")
def otro(usr):
    return f"<h1>{usr}</h1>"""
if __name__ == '__main__':
    db.create_all()
    app.run()
