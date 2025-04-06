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

def test_drop_all():

    return 

#tests creating a singular table
def test_create_table():

    return 

def test_drop_table():

    return 

def test_contains():

    return 

def test_insert():

    return 

def test_delete():

    return 

def test_update():

    return 

def test_fetch():

    return 

def test_fetch_table():

    return

def test_retrieve_data():

    return 