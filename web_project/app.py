from flask import Flask, render_template, request, redirect, url_for,session
from modols.opensearch import search_query, add_document, search, delete_all
from flask_sqlalchemy import SQLAlchemy
from utils.db import base, engine, conection_db, Session
from modols.convert_to_class import convert_to_object
import requests
import pandas as pd
from models import Clase, users
from User import User
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
@app.route('/sign_in', methods=["POST"])
def regis():
    if request.method == 'POST' and (('password' and 'email' and 'nombre' and 'apellido' and 'celular' and 'cargo' and 'direcc') in request.form):
        nombre = request.form['nombre'] + request.form['apellido']
        mail = request.form['email']
        celular = request.form['celular']
        password = request.form['password']
        universidad = request.form['universidad']
        cargo = request.form['cargo']
        direc = request.form['direcc']
        user = users(nombre, mail, password, celular, universidad, cargo, direc)
        
        # AQUI DEBE CREARSE EL USUARIO
        return render_template('index.html')
    else: 
        print("PAS MAL")
        return render_template('log_in.html')

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

@app.route('/my_profile/<usr>')
def profile(usr):
    return render_template("my_profile.html", usuario = usr)

@app.route('/log_in', methods=["POST","GET"])
def login():
    if request.method == "POST":
        logging.warning("AQUI ESTOY en post-email %s", request.form["email"])
        logging.warning("AQUI ESTOY en post-pass %s", request.form["password"])
        email = request.form['email']
        password = request.form['password']
        # buscar un usuario con ese email
        resp = engine.connect().execute(
            "SELECT * FROM users WHERE email = %s AND password = %s", email, password)
        resp = resp.fetchone()
        logging.warning("respuesta de bdd: %s", resp)
        if resp:
            user = User(resp[0], resp[1], resp[2], resp[3], 
                        resp[4], resp[5], resp[6], resp[7])
            
            # Session['user'] = user
            return render_template("my_profile.html", usuario=user)
        else:
            return render_template("log_in.html")
    else:
        return render_template("log_in.html")

# session = Session()

@app.route('/sign_in', methods=["POST", "GET"])
def signin():
    #db.session.execute(f'DROP TABLE users')
    # db.create_all()
    if request.method == "POST":
        user_name = request.form["user"]
        email = request.form["email"]
        password = request.form['password']
        universidad = request.form['uni']
        phone = request.form['phone']
        cargo = request.form['cargo']
        direc = request.form['dir']
        # agregar usuario a la base de datos
        user = users(user_name, email, password, universidad, phone, cargo, direc)
        with engine.connect() as con:
            session.add(user)
            session.commit()
            
        db.session.add(user)
        # user_id = users.query.filter_by(name=user_name).first()
        # user_id = user_id._id
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
            return render_template("sign_in.html")

            db.session.rollback()
        """
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            pass
        else:
        """
        return redirect(url_for("my_profile", usuario=user))
    else:
        return render_template("sign_in.html")

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


def page_not_found(e):
    return "<h1> Page Not Found 😦 </h1>", 404


if __name__ == '__main__':
    db.create_all()
    
    app.register_error_handler(404, page_not_found)

    app.run()
