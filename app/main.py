"""Compiles the main application."""

import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, session
from database import init_db, add_new_user, get_user_by_username
from auth import verify_login, check_email_avaliable, check_username_avaliable
from werkzeug.security import generate_password_hash

init_db()
BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, template_folder=BASE_DIR / "templates", static_folder=BASE_DIR / "static")
app.secret_key = os.urandom(24)

@app.context_processor
def inject_user():
    """Injects user information into all templates"""
    return {
        "signed_in": session.get("signed_in"),
        "username": session.get("username")
    }

@app.route("/")
def start():
    """Home Page"""
    return render_template("start.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign Up Page"""
    if request.method == "POST":

        email = request.form["email"]
        if check_email_avaliable(email) is False:
            return render_template("signup.html", email_error="Email is already taken")
        else:
            pass
        username = request.form["username"]
        if check_username_avaliable(username) is False:
            return render_template("signup.html", username_error="Username is already taken")
        else:
            pass

        password = generate_password_hash(request.form["password"])

        month, day, year = request.form["month"], request.form["day"], request.form["year"]
        if month == "mm" or day == "dd" or year == "year":
            return render_template("signup.html", dob_error="Please enter a valid date of birth")
        else:
            dob = f"{request.form['month']}/{request.form['day']}/{request.form['year']}"


        add_new_user(username, email, password, dob)
        session["signed_in"] = True
        session["username"] = username
        user = get_user_by_username(username)
        session["acct_id"] = user[0]
        return redirect("/")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Page"""
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]
        auth = verify_login(username, password)
        if auth is True:
            session["signed_in"] = True
            session["username"] = username
            user = get_user_by_username(username)
            session["acct_id"] = user[0]

            return redirect("/")
        else:
            error = True
            return render_template("login.html", error=error)

    return render_template("login.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    "Account Overview Page"
    if request.method == "POST":
        if request.form.get("signout") == "True":
            session.clear()
            return redirect("/")
        else:
            session["signed_in"] = True
            return redirect("/")
    if session.get("username") is None:
        session["signed_in"] = False
        return redirect("/")

    return render_template("account.html", user=get_user_by_username(session.get("username")))

@app.route("/coffee-fortune")
def coffee_fortune():
    """Coffee Fortune Page"""

    return render_template("coffee_fortune.html")

@app.route("/my-reviews")
def my_reviews():
    """Reviews Page"""

    return render_template("my_reviews.html")

if __name__ == "__main__":
    app.run(debug=True)
