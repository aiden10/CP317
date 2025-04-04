import random 
import string
from AuthenticationHandler import AuthenticationHandler
from Tables import Sales, Revenue, Sessions, Accounts, Inventory, Employees
from DatabaseHandler import DatabaseHandler
from datetime import datetime, timedelta
from decimal import Decimal

# Constants used as random data
SAMPLE_EMAILS = ["john.doe@example.com", "jane.smith@example.com", "bob.johnson@example.com", 
                "alice.williams@example.com", "michael.brown@example.com", "emma.jones@example.com",
                "david.miller@example.com", "sarah.davis@example.com", "james.wilson@example.com",
                "olivia.taylor@example.com"]

SAMPLE_DEPARTMENTS = ["Electronics", "Clothing", "Groceries", "Home & Garden", "Sports", 
                    "Books", "Toys", "Beauty", "Automotive", "Office Supplies"]

SAMPLE_ITEMS = ["Laptop", "Smartphone", "T-shirt", "Jeans", "Apples", "Bread", "Sofa", 
                "Lamp", "Basketball", "Tennis Racket", "Novel", "Cookbook", "Action Figure", 
                "Doll", "Shampoo", "Lipstick", "Car Battery", "Motor Oil", "Stapler", "Notebook"]

SAMPLE_CATEGORIES = ["Electronics", "Clothing", "Food", "Furniture", "Sports Equipment", 
                    "Books", "Toys", "Personal Care", "Automotive", "Office Supplies"]

SAMPLE_POSITIONS = ["Sales Associate", "Store Manager", "Assistant Manager", "Cashier", 
                    "Inventory Specialist", "Customer Service Representative", "Department Lead",
                    "Warehouse Worker", "Marketing Specialist", "IT Support"]

PRIVILEGES = ["owner", "customer", "employee"]

db_handler = DatabaseHandler()

def get_random_date() -> datetime:
	return (datetime.now() - timedelta(days=random.randint(0, 30))).date()

def populate_sales(new_rows: int) -> None:
	"""
	Populates the Sales table with random data
	:param new_rows: the amount of rows to be inserted
	"""
	for _ in range(new_rows):
		sale_row = Sales(
				date=get_random_date(),
				user=random.choice(SAMPLE_EMAILS),
				department=random.choice(SAMPLE_DEPARTMENTS),
				item=random.choice(SAMPLE_ITEMS),
				quantity=random.randint(1, 1000),
				price=random.randint(1, 100)
			)
		db_handler.insert(sale_row)

def populate_revenue(new_rows: int) -> None:
    """
    Populates the Revenue table with random data
    :param new_rows: the amount of rows to be inserted
    """
    for _ in range(new_rows):
        total_sales = round(random.uniform(100.0, 10000.0), 2)
        discounts = round(random.uniform(0.0, total_sales * 0.2), 2)
        refunds = round(random.uniform(0.0, total_sales * 0.1), 2)
        net_revenue = total_sales - discounts - refunds
        
        revenue_row = Revenue(
            date=get_random_date(),
            user=random.choice(SAMPLE_EMAILS),
            total_sales=total_sales,
            discounts=discounts,
            refunds=refunds,
            net_revenue=net_revenue
        )
        db_handler.insert(revenue_row)

def populate_sessions(new_rows: int) -> None:
    """
    Populates the Sessions table with random data
    :param new_rows: the amount of rows to be inserted
    """
    auth = AuthenticationHandler()
    for _ in range(new_rows):
        session_row = Sessions(
            session_token=auth.generate_token(),
            email=random.choice(SAMPLE_EMAILS)
        )
        db_handler.insert(session_row)

def generate_password_hash():
    """
    Generate a fake password hash
    """
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return ''.join(random.choice(chars) for _ in range(60))

def populate_accounts(new_rows: int) -> None:
    """
    Populates the Accounts table with random data
    :param new_rows: the amount of rows to be inserted
    Due to the UNIQUE constraint, this will only add rows with new emails to the table.
    """
    for _ in range(new_rows):
        account_row = Accounts(
            email=random.choice(SAMPLE_EMAILS),
            password_hash=generate_password_hash(),
            privilege=random.choice(PRIVILEGES)
        )
        db_handler.insert(account_row)

def populate_inventory(new_rows: int) -> None:
    """
    Populates the Inventory table with random data
    :param new_rows: the amount of rows to be inserted
	Due to the UNIQUE constraint, this will only add rows with new a new item to the table.
    """
    for _ in range(new_rows):
        inventory_row = Inventory(
            item_name=random.choice(SAMPLE_ITEMS),
            category=random.choice(SAMPLE_CATEGORIES),
            price=Decimal(str(round(random.uniform(5.0, 999.99), 2))),
            quantity=random.randint(0, 500)
        )
        db_handler.insert(inventory_row)

def populate_employees(new_rows: int) -> None:
    """
    Populates the Employees table with random data
    :param new_rows: the amount of rows to be inserted
    """
    first_names = ["John", "Jane", "Michael", "Emma", "David", "Sarah", "James", 
                  "Olivia", "Robert", "Elizabeth", "William", "Sophia", "Joseph", 
                  "Emily", "Thomas", "Ava", "Charles", "Mia", "Daniel", "Charlotte"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", 
                 "Wilson", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", 
                 "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark"]
    
    for i in range(new_rows):
        employee_row = Employees(
            employee_id=i + 1,
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            position=random.choice(SAMPLE_POSITIONS),
            pay=Decimal(str(round(random.uniform(15.0, 50.0), 2))),
            weekly_hours=random.choice([20.0, 30.0, 37.5, 40.0])
        )
        db_handler.insert(employee_row)

def populate_tables(rows_per_table: int):
    """
    Populates all the tables with random data
    :param rows_per_table: the approximate number of rows to insert into each table
    """
    populate_sales(rows_per_table)
    populate_revenue(rows_per_table)
    populate_sessions(rows_per_table)
    populate_accounts(rows_per_table)
    populate_inventory(rows_per_table)
    populate_employees(rows_per_table)
    view_table_counts()

def view_table_counts() -> None:
	tables = {
	"Sales": Sales,
	"Revenue": Revenue,
	"Sessions": Sessions,
	"Accounts": Accounts,
	"Inventory": Inventory,
	"Employees": Employees
	} 
	for table_name, table in tables.items():
		print(f"{table_name}: {len(db_handler.fetch_table(table=table))}")
     
if __name__ == "__main__":
    populate_tables(100)
