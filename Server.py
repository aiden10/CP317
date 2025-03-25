"""
Uses: 
    - RequestHandler
    - Logger
Called From:
    - Main

"""

"""
This file should be the one which contains the server endpoints and calls the respective RequestHandler functions for each one.
We should also have endpoints for each of the following pages:
    - Dashboard
    - Sales
    - Revenue
    - Employees
    - Inventory
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Configure SQLAlchemy with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db = SQLAlchemy()
db.init_app(app)

# route to login
@app.route("/")
def login():
    return render_template("login.html")

# route to register
# route to dashboard
# ...

if __name__ == "__main__":
    app.run(debug = True)

# ----old code
# from RequestHandler import RequestHandler
from Logger import Logger

class Server:
    def __init__(self):
        # self.request_handler = RequestHandler()
        self.logger = Logger("Server")