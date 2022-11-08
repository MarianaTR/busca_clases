from models import users
from utils.db import db
from flask import request, redirect, render_template, url_for, Blueprint

user_model = Blueprint('user_model', __name__)

@user_model.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        email = request.form["email"]
        password = request.form['password']
        user = users(user,email,password)
        print("aca")
        db.session.add(user)
        print("aca o99")
        db.session.commit()
        print("pasee")
        """
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            pass
        else:
        """
        return redirect(url_for("profile", usr=user))
    else:
        return render_template("login.html")