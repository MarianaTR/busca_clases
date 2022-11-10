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
app.secret_key = 'super-secret-key'
db = SQLAlchemy(app)


@app.route('/logout', methods=["POST", "GET"])
def logout():
    session.pop('user', None)
    session['logged_in'] = "False"
    return render_template("index.html", logged=session['logged_in'])


@app.route('/', methods=["POST","GET"])
def index():
    session['logged_in'] = "False"
    if request.method == "POST":
        busqueda = request.form["search"]
        res = search_query(busqueda)
        if res['hits']['hits']:
            value = convert_to_object(res['hits']['hits'])
        else:
            #res = search()
            value = convert_to_object(res['hits']['hits'])

        return render_template("search_result.html", clases=value, logged=session['logged_in'])
    else:
        """
        res = search()
        value = convert_to_object(res['hits']['hits'])"""
        return render_template("index.html", logged = session['logged_in'])


@app.route('/my_profile', methods=["GET"])
def profile():
    if 'user' in session:
        usr = session['user']
        logging.warning('USUARIO LOGEADO: %s', usr)
        return render_template("my_profile.html", usuario = usr)
    else:
        return render_template("log_in.html", logged=session['logged_in'])
    

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
            session['user'] = user.to_JSON()
            session['logged_in'] = 'True'

            return render_template("my_profile.html", usuario=user)
        else:
            return render_template("log_in.html", logged=session['logged_in'])
    else:
        return render_template("log_in.html", logged=session['logged_in'])

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
            session['user'] = user.to_JSON()
            session['logged_in'] = 'True'
            return render_template("my_profile.html", usuario=user)
        else:
            return render_template("sign_in.html")
    else:
        return render_template("sign_in.html")


@app.route('/create_clase', methods=['POST','GET'])
def create_clases():
    if request.method == "POST":
        name = request.form["user"]
        description = request.form["description"]
        duracion = request.form['duracion']
        precio = request.form['precio']
        modalidad = request.form['modalidad']
        user_id = session['user']['id']
        clase = Clase(user_id, name, description,duracion,precio,modalidad)
        resp = engine.connect().execute(
            'INSERT INTO clase(user_id, name, description,duracion,precio,modalidad) VALUES (%s, %s, %s, %s, %s, %s)', user_id, name, description, duracion, precio, modalidad)
        add_document(user_id,clase)
        
        return render_template("my_profile.html", usuario=session['user'])

    else:
        return  render_template("create_clase.html")

@app.route('/search', methods=['GET'])
def search():
    res = search()
    value = convert_to_object(res['hits']['hits'])
    return render_template("search_result.html", clases=value, logged=session['logged_in'])


def page_not_found(e):
    return "<h1> Page Not Found 😦 </h1>", 404


if __name__ == '__main__':
    db.create_all()
    
    app.register_error_handler(404, page_not_found)

    app.run()
