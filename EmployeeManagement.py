
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
        self.logger = Logger("EmployeeManagement")

    def get_employees(self) -> list:
        return self.db_handler.fetch_table("employees")
            
