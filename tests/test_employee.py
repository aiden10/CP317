import pytest 
from EmployeeManagement import EmployeeManagement
from DatabaseHandler import DatabaseHandler
from Tables import Employees

@pytest.fixture
def employee_handler():
    
    return EmployeeManagement()

@pytest.fixture
def db_handler():

    return DatabaseHandler()


def test_get_employee(employee_handler,db_handler):

    result = employee_handler
    employees = result.get_employees()

    assert employees is not None, "The employee table contains no data"

    #fetch the data manually from the db
    # print(employees)

    data_handler = db_handler.fetch_table("employees")


    #assert the db call from employee matches the call directly from the db

    assert data_handler == employees, "Invalid employee table doesn't match whats in db"

    return;