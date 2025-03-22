
"""
Uses: 
    - DatabaseHandler
    - Logger

Called From:
    - RequestHandler

"""

from DatabaseHandler import DatabaseHandler
from Logger import Logger

class EmployeeManagement:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger()

    def get_employees(self) -> list:
        return self.db_handler.fetch_table("employees")
            
    # Not sure how this would work because I don't know what options there are to update employees
    def update_employee(self) -> list:
        ...