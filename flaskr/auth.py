"""
user authentications views
"""

import functools
from flask import (
    Blueprint, request, redirect,url_for, render_template,flash
)
from werkzeug.security import generate_password_hash

from db import get_db

bp = Blueprint("auth", __name__,url_prefix="/auth")


@bp.route("/register",methods=("GET","POST"))
def register():
    """ user registration """

    if request.method =="POST":
        username=request.form["username"]
        password=request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "user name is required "
        elif not password:
            error="password is required"
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",(username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"user{username} is already registered"
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")

bp.route("/login",method=("GET", "POST"))
def login():

    if request.form["username"]:
        username=request.form["username"]
        password=request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username =?",(username)
        ).fetchone()

        if user is None:
            error = "incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]


