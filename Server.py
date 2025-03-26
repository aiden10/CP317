"""
Uses: 
    - RequestHandler
    - Logger
Called From:
    - Main

"""

from RequestHandler import RequestHandler
from Logger import Logger
from flask import Flask, request
from flask_cors import CORS

class Server:
    def __init__(self):
        self.request_handler = RequestHandler()
        self.logger = Logger("Server")

app = Flask(__name__)

# Configure SQLAlchemy with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'#'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
server = Server()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

# route to login
@app.post("/login")
def login():
    request_body = {
        "email": request.json.get("email"),
        "password": request.json.get("password")
    }
    
    return server.request_handler.request_login(request_body) 

# route to register
@app.post("/register")
def register():
    request_body = {
        "email": request.json.get("email"),
        "password": request.json.get("password"),
        "privilege": request.json.get("privilege")
    }
    return server.request_handler.request_registration(request_body) 

# route to logout
@app.get("/logout")
def logout():
    return server.request_handler.request_logout(request.cookies.get("session_token")) 

# route to dashboard
@app.get("/dashboard")
def dashboard():
    return server.request_handler.request_dashboard(request.cookies.get("session_token")) 

# route to sales
@app.get("/sales")
def sales():
    return server.request_handler.request_sales(request.cookies.get("session_token")) 

# route to revenue
@app.get("/revenue")
def revenue():
    return server.request_handler.request_revenue(request.cookies.get("session_token")) 

# route to employees
@app.get("/employees")
def employees():
    return server.request_handler.request_employees(request.cookies.get("session_token")) 

# route to inventory
@app.get("/inventory")
def inventory():
    return server.request_handler.request_inventory(request.cookies.get("session_token")) 

# route to inventory_order
@app.post("/inventory/order")
def inventory_order():
    request_body = {
        "quatity": request.json.get("quantity"),
        "product_name": request.json.get("quantity"),
        "session_token": request.cookies.get("session_token")
    }

    return server.request_handler.request_inventory_order(request_body) 

if __name__ == "__main__":
    app.run(debug = True, port=8000)
