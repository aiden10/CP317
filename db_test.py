# Imports
from Tables import Sales, Revenue
from DatabaseHandler import DatabaseHandler
from datetime import datetime as dt

# Testing the DatabaseHandler
if __name__ == "__main__":
    db_handler = DatabaseHandler()
    db_handler.create_tables()
    #db_handler.drop_all() # Clear the ENTIRE database

    # Insert a sales record
    new_sale = Sales(date=dt.now().date(), user="Joanna Doe", department = "dairy", item="cheese", quantity=1, price=1500.0)
    db_handler.insert(new_sale)

    # Insert a revenue record
    new_revenue = Revenue(date=dt.now().date(), total_sales=1500.0, discounts=100.0, refunds=0.0, net_revenue=1400.0)
    db_handler.insert(new_revenue)

    # Fetch all sales
    sales_data = db_handler.fetch_table(Sales)
    print("Sales Data:", sales_data)

    # Update a sales record
    db_handler.update(Sales, {"user": "John Doe"}, {"quantity": 2})

    # Fetch updated record
    updated_sale = db_handler.fetch(Sales, {"user": "John Doe"})
    print("Updated Sale:", updated_sale)

    # Delete a sales record
    #db_handler.delete(Sales, {"user": "John Doe"})

    # Fetch all revenue records
    revenue_data = db_handler.fetch_table(Revenue)
    print("Revenue Data:", revenue_data)

    # Now test with limited permissions of user (only return their own sales)
    user = "customer"
    name = "John Doe"

    print("all my records:", db_handler.fetch(Sales, {"user":name}))
