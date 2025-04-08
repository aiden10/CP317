import pytest
from DatabaseHandler import DatabaseHandler
from sqlalchemy import create_engine
from sqlalchemy import inspect


@pytest.fixture
def db_handler():
    engine = create_engine("sqlite:///database.db")
    data_handler =  DatabaseHandler()
    data_handler.engine = engine

    return data_handler


def test_create_tables(db_handler):
    table_names = ["sales","accounts","sessions","employees","revenue","Inventory","assets"]

    db_handler.create_tables()

    inspector = inspect(db_handler.engine)

    tables = inspector.get_table_names()



    for i in table_names:
        print(tables)
        assert i in tables, f"Table '{i}' does not exist after create_tables is invoked"

    print("All tables exist after create_tables is invoked")


    return 

def test_drop_all(db_handler):
    # Drop all tables
    db_handler.drop_all()

    # Inspecting the database schema after dropping tables
    inspector = inspect(db_handler.engine)
    tables = inspector.get_table_names()

    # Check that all tables are dropped
    assert len(tables) == 0, "Tables still exist after drop_all is invoked"

    print("All tables are dropped after drop_all is invoked")

#tests creating a singular table
def test_create_table(db_handler):
    # Create a single table (for example: sales)
    db_handler.create_table('sales')

    # Inspect the database schema to check if the 'sales' table exists
    inspector = inspect(db_handler.engine)
    tables = inspector.get_table_names()

    assert "sales" in tables, "Table 'sales' does not exist after create_table is invoked"
    print("Table 'sales' exists after create_table is invoked")

def test_drop_table(db_handler):
    # Drop the 'sales' table
    db_handler.drop_table('sales')

    # Inspect the database schema to check if the 'sales' table exists
    inspector = inspect(db_handler.engine)
    tables = inspector.get_table_names()

    assert "sales" not in tables, "Table 'sales' still exists after drop_table is invoked"
    print("Table 'sales' is dropped after drop_table is invoked") 

def test_contains(db_handler):
    # Insert some data into the sales table
    db_handler.insert('sales', {'item': 'Apple', 'quantity': 100, 'price': 1.50})

    # Fetch the data and check if it exists
    result = db_handler.fetch('sales', {'item': 'Apple'})
    
    assert len(result) > 0, "Data does not exist in 'sales' table"
    assert result[0]['item'] == 'Apple', "The data in 'sales' table does not match"
    print("Data exists in the 'sales' table as expected")

def test_insert(db_handler):
    # Insert data into the 'sales' table
    db_handler.insert('sales', {'item': 'Banana', 'quantity': 150, 'price': 0.75})

    # Fetch the inserted data to verify
    result = db_handler.fetch('sales', {'item': 'Banana'})
    
    assert len(result) > 0, "Data insertion failed in 'sales' table"
    assert result[0]['item'] == 'Banana', "Inserted data does not match"
    print("Data inserted into 'sales' table successfully")

def test_delete(db_handler):
    # Insert a record into the 'sales' table for deletion
    db_handler.insert('sales', {'item': 'Grapes', 'quantity': 50, 'price': 2.00})

    # Delete the record
    db_handler.delete('sales', {'item': 'Grapes'})

    # Verify that the record has been deleted
    result = db_handler.fetch('sales', {'item': 'Grapes'})
    
    assert len(result) == 0, "Data was not deleted from 'sales' table"
    print("Data deleted from 'sales' table successfully")

def test_clear_table(db_handler):
    # Insert records into the 'sales' table
    db_handler.insert('sales', {'item': 'Peach', 'quantity': 20, 'price': 3.00})
    db_handler.insert('sales', {'item': 'Pineapple', 'quantity': 30, 'price': 2.50})

    # Clear all records from the 'sales' table
    db_handler.clear_table('sales')

    # Fetch the records to verify the table is empty
    result = db_handler.fetch('sales', {})
    
    assert len(result) == 0, "Records were not cleared from 'sales' table"
    print("All records cleared from 'sales' table successfully")

def test_update(db_handler):
    # Insert a record into the 'sales' table for updating
    db_handler.insert('sales', {'item': 'Mango', 'quantity': 80, 'price': 1.25})

    # Update the record
    db_handler.update('sales', {'item': 'Mango'}, {'price': 1.50, 'quantity': 100})

    # Fetch the updated data to verify the change
    result = db_handler.fetch('sales', {'item': 'Mango'})
    
    assert result[0]['price'] == 1.50, "Price update failed"
    assert result[0]['quantity'] == 100, "Quantity update failed"
    print("Data updated successfully in 'sales' table")

def test_fetch(db_handler):
    # Insert a record into the 'sales' table for fetching
    db_handler.insert('sales', {'item': 'Apple', 'quantity': 100, 'price': 1.50})

    # Fetch the inserted data based on item name
    result = db_handler.fetch('sales', {'item': 'Apple'})
    
    # Verify the fetched data matches the inserted data
    assert len(result) > 0, "No data returned for 'Apple'"
    assert result[0]['item'] == 'Apple', "Fetched item does not match"
    assert result[0]['quantity'] == 100, "Fetched quantity does not match"
    assert result[0]['price'] == 1.50, "Fetched price does not match"
    
    print("Data fetched correctly for 'Apple' in 'sales' table")
def test_fetch_table(db_handler):
    # Insert multiple records into the 'sales' table for fetching all data
    db_handler.insert('sales', {'item': 'Apple', 'quantity': 100, 'price': 1.50})
    db_handler.insert('sales', {'item': 'Banana', 'quantity': 150, 'price': 0.75})

    # Fetch all records from the 'sales' table
    result = db_handler.fetch_table('sales')
    
    # Verify the fetched data contains the inserted records
    assert len(result) > 1, "No data returned from 'sales' table"
    assert any(record['item'] == 'Apple' for record in result), "'Apple' not found in fetched data"
    assert any(record['item'] == 'Banana' for record in result), "'Banana' not found in fetched data"
    
    print("Data fetched correctly from 'sales' table")


def test_retrieve_data(db_handler):
    # Insert multiple records into the 'sales' table
    db_handler.insert('sales', {'item': 'Apple', 'quantity': 100, 'price': 1.50})
    db_handler.insert('sales', {'item': 'Banana', 'quantity': 150, 'price': 0.75})

    # Retrieve data for a specific item, such as 'Apple'
    result = db_handler.retrieve_data('sales', {'item': 'Apple'})
    
    # Verify the retrieved data matches the conditions
    assert len(result) == 1, "Expected only 1 record for 'Apple'"
    assert result[0]['item'] == 'Apple', "Retrieved item does not match"
    assert result[0]['quantity'] == 100, "Retrieved quantity does not match"
    assert result[0]['price'] == 1.50, "Retrieved price does not match"
    
    print("Specific data retrieved correctly for 'Apple' from 'sales' table")
