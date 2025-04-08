import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from time import strftime
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

rows = []

# Ensure templates are auto-reloaded
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    rows = db.execute("SELECT symbol, name, shares FROM stocks\
        WHERE user_id = :user_id order by symbol",\
        user_id = session["user_id"])

    stock_total = 0
    for row in rows:
        current_price = lookup(row["symbol"])["price"]
        total = current_price*int(row["shares"])
        row["current_price"] = usd(current_price)
        row["total"] = usd(total)
        stock_total += total

    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",\
        user_id = session["user_id"])[0]["cash"]

    total = cash + stock_total

    return render_template("portfolio.html", rows = rows,\
        cash = usd(cash), total = usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))  # lookup price here

        if not request.form.get("symbol"):  # user input a stock’s symbol
            return apology("Missing symbol")

        elif not quote:
            return apology("Invalid symbol")

        # Require that a user input a number of shares, implemented as a field whose name is shares
        elif not request.form.get("shares"):
            return apology("Missing shares")

        elif not str.isdigit(request.form.get("shares")):
            return apology("Invalid shares")

        elif not int(request.form.get("shares")) <= 0:
            return apology("Invalid shares")

        name = quote["name"]

        rows = db.execute("SELECT cash FROM users WHERE id =:id", id=session["user_id"])

        price_per_share = quote["price"]

        total_price = float(price_per_share)*int(request.form.get("shares"))

        available_cash = float(db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"])

        # Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price
        if available_cash < total_price:
            return apology("Insufficient funds")

        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=available_cash - total_price, id=session["user_id"])

            datetime = strftime('%Y-%m-%d %H:%M:%S')

            flash("Transaction complete")

            # update history
            db.execute("""INSERT INTO transactions (
                user_id, symbol, name, shares, price_per_share, total_price, transacted)
                VALUES(:user_id, :symbol, :name, :shares, :price_per_share, :total_price, :transacted)""",\
                user_id = session["user_id"], symbol=str.upper(request.form.get("symbol")),\
                name = name, shares=int(request.form.get("shares")), price_per_share=price_per_share,\
                total_price = total_price, transacted=datetime)

            instock = db.execute("SELECT symbol FROM stocks WHERE user_id = :user_id and symbol = :symbol", user_id=session["user_id"],\
                symbol=str.upper(request.form.get("symbol")))

            if not instock:
                db.execute("""INSERT INTO stocks (
                    user_id, symbol, name, shares)
                    VAUES(:user_id, symbol, :name, :shares)""",\
                    user_id = session["user_id"], symbol=str.upper(request.form.get("symbol")),\
                    name = name, shares=int(request.form.get("shares")))

            else:
                rows = db.execute("SELECT shares FROM stocks WHERE user_id = :user_id and symbol = :symbol",\
                    user_id = session["user_id"], symbol=str.upper(request.form.get("symbol")))

                db.execute("UPDATE stocks SET shares = :shares\
                    WHERE user_id = :user_id and symbol = :symbol",\
                    shares = int(rows[0]["shares"]) + int(request.form.get("shares")),\
                    user_id = session["user_id"], symbol=str.upper(request.form.get("symbol")))

        return redirect("/")  # redirect to homepage

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT symbol, name, shares, price_per_share, total_price, transacted FROM transactions\
        WHERE user_id = :user_id", user_id=session["user_id"])

    for row in rows:
        row["price_per_share"] = usd(row["price_per_share"])
        row["total_price"] = usd(row["total_price"])

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":  # Submit the user’s input via POST to /quote

        if not request.form.get("symbol"):  # user input a stock’s symbol, implemented as a text field whose name is symbol
            return apology("Missing symbol")
        else:
            quote = lookup(request.form.get("symbol"))  # helpers.py

        if not quote:
            return apology("Invalid symbol")
        else:
            return render_template("quoted.html", quote=quote, price=usd(quote["price"]))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()  # forget user ID

    if request.method == "POST":
        # checks for username
        if not request.form.get("username"):
            return apology("Provide a username")

        # checks for password
        elif not request.form.get("password"):
            return apology("Provide a password")

        # checks password is repeated
        elif not request.form.get("confirmation"):
            return apology("Repeat password")

        # checks both passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        # check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if len(rows) == 1:
            return apology("Username already taken")
        else:
            # add to database
            db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)",\
                username = request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
            flash("You are now registered")

            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

            session["user_id"] = rows[0]["id"]

            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":  # Submit the user’s input via POST to /sell

        # Require that a user input a stock’s symbol, implemented as a select menu whose name is symbol.
        quote = lookup(request.form.get("symbol"))

        # Render an apology if the user fails to select a stock or if (somehow, once submitted) the user does not own any shares of that stock.
        if not request.form.get("symbol"):
            return apology("Missing symbol")

        elif not quote:
            return apology("Invalid symbol")
    # Require that a user input a number of shares, implemented as a field whose name is shares.
        # Render an apology if the input is not a positive integer or if the user does not own that many shares of the stock.
        elif not request.form.get("shares"):
            return apology("Missing shares")

        elif int(request.form.get("shares")) <= 0:
            return apology("Invalid shares")

        name = quote["name"]

        rows = db.exectue("SELECT shares FROM stocks WHERE user_id = :id and symbol = :symbol",\
            id = session["user_id"], symbol=str.upper(request.form.get("symbol")))

        if not rows or int(request.form.get("shares")) > int(rows[0]["shares"]):
            return apology("Not enough shares")

        else:
            if int(rows[0]["shares"]) == int(request.form.get("shares")):
                db.execute("DELETE FROM stocks WHERE user_id = :user_id and symbol = :symbol", user_id=session["user_id"],\
                    symbol=str.upper(request.form.get("symbol")))

            db.execute("""UPDATE stocks SET shares = :shares WHERE user_id = :user_id and symbol = :symbol""",\
                shares = int(rows[0]["shares"]) - int(request.form.get("shares")),\
                user_id = session["user_id"], symbol=str.upper(request.form.get("symbol")))

            flash("Transaction successful")

            price_per_share = float(quote["price"])
            total_value = price_per_share*int(request.form.get("shares"))

            datetime = strftime('%Y-%m-%d %H:%M:%S')

            db.execute("""INSERT INTO transactions(
                user_id, symbol, name, shares, price_per_share, total_price, transacted)
                VALUES(:user_id, :symbol, :name, :shares, :price_per_share, :total_price, :transacted)""",\
                user_id = session["user_id"], symbol=str.upper(request.form.get("symbol")),\
                name = name, shares = "-" + request.form.get("shares"), price_per_share=price_per_share, \
                total_price = total_value, transacted=datetime)

            rows = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = rows[0]["cash"] + total_value, id = session["user_id"])

            return redirect("/")  # Upon completion, redirect the user to the home page.

    else:
        return render_template("sell.html")


@login_required
def add_cash():
    """Add cash to the account"""

    if request.method == "POST":

        if not request.form.get("add_cash"):
            return apology("Missing amount of cash")

        elif not str.isdigit(request.form.get("add_cash")) or float(request.form.get("add_cash")) < 0.01\
            or float(request.form.get("add_cash")) > 100000:
            return apology("Invalid amount")

        rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=rows[0]["cash"] + float(request.form.get("add_cash")),\
            id = session["user_id"])

        return redirect("/")

    else:
        return render_template("add_cash.html")