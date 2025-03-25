from Server import db

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
    total_sales = db.Column(db.Float, nullable=False) # aggregated by day
    discounts = db.Column(db.Float, nullable=True, default=0.0)
    refunds = db.Column(db.Float, nullable=True, default=0.0)
    net_revenue = db.Column(db.Float, nullable=False) # total_sales - discounts - refunds