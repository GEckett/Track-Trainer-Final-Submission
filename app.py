from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

# Configure application
app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

if __name__ == "__main__":
    app.run(debug=True)