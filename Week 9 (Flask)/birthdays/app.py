import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        if name.isdigit():
            return redirect("/")
        month = request.form.get("month")
        day = request.form.get("day")
        if datetime(year=2024,month=int(month),day=int(day)) == "ValueError":
            return redirect("/")
        db.execute("INSERT INTO birthdays (name,month,day) VALUES (?,?,?)",name,month,day)
        return render_template("index.html",registrants = db.execute("SELECT name,month,day FROM birthdays"))
    else:
        # TODO: Display the entries in the database on index.html
        return render_template("index.html",registrants = db.execute("SELECT name,month,day FROM birthdays"))


