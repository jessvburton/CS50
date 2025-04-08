import os
import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

rows = []

# Ensure templates are auto-reloaded
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db_p = SQL("sqlite:///pokemon.db")
db_t = SQL("sqlite:///types.db")

row = []

# Helper functions
def get_db_pokemon():
    con = sqlite3.connect('pokemon.db')
    con.row_factory = sqlite3.Row
    return con

def get_db_types():
    con = sqlite3.connect('types.db')
    con.row_factory = sqlite3.Row
    return con

def get_users(search):
    con = sqlite3.connect('pokemon.db')
    cursor = con.cursor()
    cursor.execute(
        "SELECT \"#\", name, group_CONCAT(type, ', ') as Types, total, hp, attack, defense, \"special attack\", \"special defense\", speed from pokemon WHERE name LIKE ? OR type LIKE ? group by name",
        ("%"+search+"%", "%"+search+"%",)
        )
    results = cursor.fetchall()
    con.close()
    return results

def create_sql_script(types):
    script = "SELECT attack"
    defenses = set()

    # Get all the distinct defense entries
    con = sqlite3.connect('types.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT DISTINCT defense FROM types")
    defenses = [row[0] for row in cursor.fetchall()]

    # Generate the script using the distinct defense entries
    for defense in defenses:
        script += f",MAX(CASE WHEN defense = '{defense}' then multiplier END) AS {defense}"

    script += f" from types group BY attack order BY attack ASC;"
    return script

# Webpages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if not request.form.get("search"):
        con = get_db_pokemon()
        data = con.execute("SELECT \"#\", name, group_CONCAT(type, ', ') as Types, total, hp, attack, defense, \"special attack\", \"special defense\", speed from pokemon group by name order by name").fetchall()
        con.close()
        return render_template('search.html', data=data)
    elif request.form.get("search"):
        data = dict(request.form)
        pokemon = get_users(data["search"])
    else:
        pokemon = []

    return render_template('results.html', pokemon=pokemon)


@app.route("/results", methods=["GET","POST"])
def results():
    if request.method == "POST":
        data = dict(request.form)
        pokemon = get_users(data["search"])
    else:
        pokemon = []

    return render_template('results.html', pokemon=pokemon)

@app.route("/types")
def types():
    sql_script = create_sql_script("types")

    con = sqlite3.connect('types.db')
    cursor = con.cursor()
    data = cursor.execute(sql_script).fetchall()

    return render_template("types.html", data=data)

@app.route("/compare", methods=["GET","POST"])
def compare():
    option1 = request.form.get("option1")
    option2 = request.form.get("option2")

    if option1 == option2:
        flash('The two entries are the same!')

    return render_template('compare.html')


@app.route("/comparison", methods=["GET","POST"])
def comparison():
    if request.method == "POST":
        data = dict(request.form)
        pokemon1 = get_users(data["option1"])
        pokemon2 = get_users(data["option2"])
    else:
        return render_template('compare.html')

    return render_template('comparison.html', pokemon1=pokemon1, pokemon2=pokemon2)