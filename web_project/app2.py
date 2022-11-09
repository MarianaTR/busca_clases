from flask import Flask, render_template, request, redirect, url_for, session
from modols.opensearch import search_query, add_document, search, delete_all
from flask_sqlalchemy import SQLAlchemy
from utils.db import base, engine, conection_db
from modols.convert_to_class import convert_to_object
import requests
import pandas as pd
from models import Clase, users
from User import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/ping')
def do_ping():
    ping = 'Ping ...'

    response = ''
    try:
        response = requests.get(
            'http://opensearch_node1:9200/iaps-index/_search')
        print(response.text)
    except requests.exceptions.RequestException as e:
        print('\n Cannot reach the pong service.')
        return 'Ping ...\n'

    return 'Ping ... ' + response.text + ' ' + str(type(response))+' \n'


@app.route('/', methods=["POST", "GET"])
def index():
    # delete_all()
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


@app.route('/busqueda', methods=["POST", "GET"])
def hello_world():  # put application's code here
    print("aqui")


@app.route('/my_profile/<usr>')
def profile(usr):
    # usr = users.query.filter_by(_id = usr).first()
    return render_template("my_profile.html", usr=usr)


@app.route('/log_in', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print("AQUI---1 . ENTRE AL POST")
        email = request.form["email"]
        password = request.form['password']
        # buscar un usuario con ese email
        with engine.connect() as con:
            print("AQUI---2 . ENTRE AL ENGINE")
            con.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s", email, password)
            result = con.fetchall()
            print("AQUI---3 RESULT", result)
            # for row in result:
            #     user = User(row[0], row[1], row[2], row[3],
            #                 row[4], row[5], row[6], row[7])

            con.close()
        # if user:
        #     return render_template("profile.html", usr=user)
        # else:
        #     return render_template("log_in.html")
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
        user = users(user_name, email, password,
                     universidad, phone, cargo, direc)
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
        return redirect(url_for("my_profile", usr=user))
    else:
        return render_template("sign_in.html")


@app.route('/admin')
def admin():
    return render_template("view.html", values=Clase.query.all())


@app.route('/create_class/<user>', methods=['POST', 'GET'])
def create_clases(user):
    db.create_all()
    if request.method == "POST":
        name = request.form["user"]
        description = request.form["description"]
        duracion = request.form['duracion']
        precio = request.form['precio']
        modalidad = request.form['modalidad']
        user_id = user
        clase = Clase(user_id, name, description, duracion, precio, modalidad)
        db.session.add(clase)
        db.session.commit()
        add_document(user_id, clase)
        return redirect(url_for("index"))
    else:
        return render_template("create_clase.html")


def page_not_found(e):
    return "<h1> Page Not Found 😦 </h1>", 404


"""@app.route("/<usr>")
def otro(usr):
    return f"<h1>{usr}</h1>"""
if __name__ == '__main__':
    db.create_all()

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_not_found)

    app.run()
