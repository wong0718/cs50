import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    holdings = db.execute("SELECT symbol,SUM(shares) as shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",user_id)

    stocks = []
    real_total = 0

    for holding in holdings:
        symbol = holding['symbol']
        shares = holding['shares']
        stocks_info = lookup(symbol)

        if stocks_info:
            price = stocks_info['price']
            total = shares * price
            real_total += total

        stocks.append({
            'symbol': symbol,
            'shares': shares,
            'price': price,
            'total': shares * price
        })

    db_cash = db.execute("SELECT cash FROM users WHERE id = ?",user_id)
    cash = db_cash[0]['cash']

    real_total += cash
    # stocks = db.execute("SELECT symbol,SUM(shares) as shares,price,transaction_date FROM transactions WHERE user_id = ? GROUP BY symbol",user_id)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if request.form.get("buy") != None:
            if lookup(symbol) == None:
                return apology("Invalid symbol")
            elif symbol:
                stock = lookup(symbol)
                total_cost = float(stock['price']) * int(shares)
                total_cost = round(total_cost,2)
                if total_cost > cash:
                    return apology("Insufficient funds")
                db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",total_cost,user_id)
                db.execute("INSERT INTO transactions (symbol,shares,price,user_id,transaction_date) VALUES (?,?,?,?,?)",stock['symbol'],shares,stock['price'],session["user_id"],datetime.now())
                return redirect("/")
            elif shares < 1:
                return apology("Invalid number of shares")

        elif request.form.get("sell") != None:
            symbol = request.form.get("symbol")
            shares = request.form.get("shares")
            if symbol is None:
                return apology("Please provide a symbol")

            owned = db.execute(
                "SELECT symbol,SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? HAVING SUM(shares) > 0",
                user_id,
                symbol
            )

            if not owned or owned[0]['symbol'] is None:
                return apology("Symbol not owned")

            if int(shares) > owned[0]['total_shares']:
                return apology("Not enough shares")
            checker = lookup(symbol)
            total_cost = float(checker['price']) * int(shares)
            total_cost = round(total_cost,2)
            shares = int(shares) * -1
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",total_cost,user_id)
            db.execute("INSERT INTO transactions (symbol,shares,price,user_id,transaction_date) VALUES (?,?,?,?,?)",checker['symbol'],shares,checker['price'],session["user_id"],datetime.now())
            return redirect("/")
        else:
            stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY symbol ",
            user_id
            )
    else:
        return render_template("index.html",stocks = stocks,cash = cash,total = real_total)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must provide symbol", 400)

        if not shares:
            return apology("Must provide shares", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Shares must be positive", 400)
        except ValueError:
            return apology("Shares must be a number", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol", 400)

        db_cash = db.execute("SELECT cash FROM users WHERE id = ?",user_id)
        cash = db_cash[0]['cash']

        total_cost = float(stock['price']) * int(shares)
        total_cost = round(total_cost,2)
        if total_cost > cash:
            return apology("Insufficient funds")
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",total_cost,user_id)
        db.execute("INSERT INTO transactions (symbol,shares,price,user_id,transaction_date) VALUES (?,?,?,?,?)",stock['symbol'],shares,stock['price'],session["user_id"],datetime.now())
        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    return render_template("history.html",records = db.execute("SELECT symbol,shares,price,transaction_date FROM transactions WHERE user_id = ? ORDER BY transaction_date DESC",user_id))

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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "POST":
        query = request.form.get("quote")
        if lookup(query) == None:
            return apology("Invalid symbol/No symbol")
        else:
            stock = lookup(query)
            return render_template("quoted.html",stock = stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        user_id = session["user_id"]
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please enter a username", 400)

        existing = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing:
            return apology("Username already exists", 400)

        if not password:
            return apology("Please enter a password", 400)

        if len(password) < 8:
            return apology("Password must be at least 8 characters", 400)

        if not confirmation:
            return apology("Please enter your confirmation")

        if password != confirmation:
            return apology("Passwords do not match", 400)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)",username,hash)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please provide a symbol",400)

        if not shares:
            return apology("Must provide shares", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Shares must be positive", 400)
        except ValueError:
            return apology("Shares must be a number", 400)

        owned = db.execute(
            "SELECT symbol,SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? HAVING SUM(shares) > 0",
            user_id,
            symbol
        )

        if not owned or owned[0]['symbol'] is None:
            return apology("Symbol not owned")

        if int(shares) > owned[0]['total_shares']:
            return apology("Not enough shares")

        checker = lookup(symbol)
        if not checker:
            return apology("Unable to fetch stock price", 500)

        total_cost = float(checker['price']) * int(shares)
        total_cost = round(total_cost,2)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",total_cost,user_id)
        db.execute("INSERT INTO transactions (symbol,shares,price,user_id,transaction_date) VALUES (?,?,?,?,?)",checker['symbol'],-shares,checker['price'],session["user_id"],datetime.now())
        flash("Sold!")
        return redirect("/")
    else:
        stocks = db.execute(
        "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY symbol ",
        user_id
        )
        return render_template("sell.html",stocks=stocks)

@app.route("/password",methods=["GET","POST"])
@login_required
def password():
    """Change password"""
    user_id = session["user_id"]
    if request.method == "POST":
        old_password = request.form.get("old-password")
        new_password = request.form.get("new-password")
        confirmation = request.form.get("confirmation")

        if not old_password:
            return apology("Must provide old password", 400)
        if not new_password:
            return apology("Must provide new password", 400)
        if not confirmation:
            return apology("Must confirm new password", 400)

        db_user_password = db.execute("SELECT hash FROM users WHERE id = ?",user_id)
        checker = check_password_hash(db_user_password[0]['hash'],old_password)
        if checker == False:
            return apology("Wrong old passsword")

        if len(new_password) < 8:
            return apology("Password must be at least 8 characters", 400)

        if old_password == new_password:
            return apology("New password must be different", 400)

        if new_password != confirmation:
            return apology("Passwords do not match", 400)

        hash = generate_password_hash(new_password)
        if old_password == new_password:
            return apology("New password can't be same as old password ")

        hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?",hash,user_id)

        flash("Password changed successfully!")
        return redirect("/")
    else:
        return render_template("password.html")

@app.route("/funds",methods=["GET","POST"])
@login_required
def funds():
    user_id = session["user_id"]
    if request.method == "POST":
        funds = request.form.get("funds")
        cash = db.execute("SELECT cash FROM users WHERE id = ?",user_id)

        if not funds:
            return apology("Must provide amount", 400)

        try:
            funds = int(funds)
        except ValueError:
            return apology("Amount must be a number", 400)

        if cash[0]['cash'] < funds:
            return apology("Not enough cash to take out",400)
        if funds < 0:
            return apology("Funds can't be negative",400)

        if request.form.get("add") != None:
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",funds,user_id)
            db.execute("INSERT INTO transactions (symbol,shares,price,user_id,transaction_date) VALUES (?,?,?,?,?)",None,None,funds,session["user_id"],datetime.now())
            flash(f"Added {usd(funds)} to account!")
        elif request.form.get("remove") != None:
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",funds,user_id)
            db.execute("INSERT INTO transactions (symbol,shares,price,user_id,transaction_date) VALUES (?,?,?,?,?)",None,None,-funds,session["user_id"],datetime.now())
            flash(f"Withdrew {usd(funds)} from account!")

        return redirect ("/")
    else:
        return render_template("funds.html")
