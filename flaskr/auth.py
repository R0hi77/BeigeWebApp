"""
user authentications views
"""

import functools
from flask import (
    Blueprint, request, redirect,url_for, render_template,flash,session,g
)
from werkzeug.security import generate_password_hash, check_password_hash

from . db import get_db

bp = Blueprint("auth", __name__,url_prefix="/auth")


@bp.route("/register",methods=("GET","POST"))
def register():
    """ User registration """

    if request.method == "POST":
        username=request.form["username"]
        password=request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "username is required "
        elif not password:
            error=  "password is required"
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"user{username} is already registered"
            finally:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")



@bp.route("/login",methods=("GET","POST"))
def login():
    """ Handles user Log in """

    if request.method == "POST":
        username=request.form["username"]
        password=request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?",(username,)
        ).fetchone()

        if user is None:
            error = "incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "incorrect password"
             

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        
        flash(error)
         
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    """ check if the request is from the user"""
    user_id = session.get("user_id",None)
    db = get_db()
    if user_id == None:
        g.user = None 
    else:
        g.user = db.execute(
            'SELECT * FROM user WHERE id =?',(user_id,)
        ).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
        
         