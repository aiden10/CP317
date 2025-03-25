from DatabaseHandler import db

class Sales(db.Model):
    __tablename__ = "Sales"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    user = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable=False)

class Revenue(db.Model):
    __tablename__ = "Revenue"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    user = db.Column(db.String(100), nullable=False)
    total_sales = db.Column(db.Float, nullable=False) # aggregated by day
    discounts = db.Column(db.Float, nullable=True, default=0.0)
    refunds = db.Column(db.Float, nullable=True, default=0.0)
    net_revenue = db.Column(db.Float, nullable=False) # total_sales - discounts - refunds

class Sessions(db.Model):
    __tablename__ = "sessions"
    session_token = db.Column(db.String(512), primary_key=True)
    email = db.Column(db.String(255))

class Accounts(db.Model):
    __tablename__ = "accounts"
    email = db.Column(db.String(255), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    privilege = db.Column(db.String(12), nullable=True)


class Inventory(db.Model):
    __tablename__ = "inventory"
    item_name = db.Column(db.String(255), primary_key=True)
    category = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Numeric(19, 4), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Employees(db.Model):
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=True)
    pay = db.Column(db.Numeric(19, 4), nullable=False)
    weekly_hours = db.Column(db.Float, nullable=True)

