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

global_user = None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/logout', methods=["POST", "GET"])
def logout():
    global_user = None
    return render_template("index.html")


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


@app.route('/my_profile', methods=["GET"])
def profile(usr=global_user):
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
            global_user = user
            # Session['user'] = user
            return render_template("my_profile.html", usuario=user)
        else:
            return render_template("log_in.html")
    else:
        return render_template("log_in.html")

@app.route('/sign_in', methods=["POST","GET"])
def regis():
    logging.warning("antes de entrar a post")
    if request.method == 'POST' and (('password' and 'email' and 'nombre' and 'apellido' and 'celular' and 'cargo' and 'direcc') in request.form):
        logging.warning('entre al post')
        nombre = request.form['nombre'] +" "+ request.form['apellido']
        mail = request.form['email']
        celular = request.form['celular']
        password = request.form['password']
        universidad = request.form['univer']
        cargo = request.form['cargo']
        direc = request.form['direcc']
        
        #agregar a la base de datos un usuario
        logging.warning("antes de insert:")
        resp = engine.connect().execute(
            'INSERT INTO users(name, email, password, phone, universidad, cargo, direcc) VALUES (%s, %s, %s, %s, %s, %s, %s)', nombre, mail, password, celular, universidad, cargo, direc)
        resp = engine.connect().execute(
            "SELECT * FROM users WHERE email = %s AND password = %s", mail, password)
        resp = resp.fetchone()
        logging.warning("respuesta de bdd: %s", resp)
        if resp:
            user = User(resp[0], resp[1], resp[2], resp[3],
                        resp[4], resp[5], resp[6], resp[7])
            global_user = user
            return render_template("my_profile.html", usuario=user)
        else:
            return render_template("sign_in.html")
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
