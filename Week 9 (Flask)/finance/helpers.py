import requests

from cs50 import SQL
from flask import redirect, render_template, session, flash
from functools import wraps
from datetime import datetime

db = SQL("sqlite:///finance.db")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        quote_data = response.json()
        return {
            "name": quote_data["companyName"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def validate_trade_inputs(symbol,shares):
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
    return int(shares)



def get_user_portfolio(user_id):
    """Get user's complete portfolio with current prices"""
    holdings = db.execute(
        "SELECT symbol, SUM(shares) as shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        user_id
    )

    stocks = []
    stocks_total = 0

    for holding in holdings:
        symbol = holding['symbol']
        shares = holding['shares']
        stock_info = lookup(symbol)

        if stock_info:
            price = stock_info['price']
            total = shares * price
            stocks_total += total

            stocks.append({
                'symbol': symbol,
                'shares': shares,
                'price': price,
                'total': total
            })

    cash = get_user_cash(user_id)
    grand_total = stocks_total + cash

    return stocks, cash, grand_total

def get_user_shares(user_id,symbol):
    """Get number of shares user owns for a specific symbol"""
    result = db.execute(
        "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?",
        user_id, symbol
    )

    if result and result[0]['total_shares']:
        return result[0]['total_shares']
    return 0

def get_user_cash(user_id):
    result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    return result[0]['cash'] if result else 0


def execute_buy(user_id,symbol,shares):
    """Execute a buy transaction"""
    stock = lookup(symbol)
    if not stock:
        return apology("Invalid symbol", 400)

    cash = get_user_cash(user_id)
    total_cost = stock['price'] * shares

    if total_cost > cash:
        return apology("Insufficient funds", 400)

    # Execute purchase
    db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
    db.execute(
        "INSERT INTO transactions (symbol, shares, price, user_id, transaction_date) VALUES (?, ?, ?, ?, ?)",
        stock['symbol'], shares, stock['price'], user_id, datetime.now()
    )

    flash(f"✓ Bought {shares} shares of {symbol} for {usd(total_cost)}")
    return None



def execute_sell(user_id,symbol,shares):
    owned_shares = get_user_shares(user_id, symbol)

    if owned_shares < shares:
        return apology(f"You only own {owned_shares} shares of {symbol}", 400)

    stock = lookup(symbol)
    if not stock:
        return apology("Unable to fetch stock price", 500)

    total_proceeds = stock['price'] * shares

    # Execute sale
    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_proceeds, user_id)
    db.execute(
        "INSERT INTO transactions (symbol, shares, price, user_id, transaction_date) VALUES (?, ?, ?, ?, ?)",
        stock['symbol'], -shares, stock['price'], user_id, datetime.now()
    )

    flash(f"✓ Sold {shares} shares of {symbol} for {usd(total_proceeds)}")
    return None

