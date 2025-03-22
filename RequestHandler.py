
"""
Uses: 
    - AuthenticationHandler
    - DashboardSummarizer
    - FinanceModule
    - EmployeeManagement
    - InventoryManagement
    - Logger

Called From:
    - Server

"""

from AuthenticationHandler import AuthenticationHandler
from DashboardSummarizer import DashboardSummarizer
from FinanceModule import FinanceModule
from EmployeeManagement import EmployeeManagement
from InventoryManagement import InventoryManagement
from Logger import Logger

class RequestHandler:
    def __init__(self):
        self.auth_handler = AuthenticationHandler()
        self.dashboard = DashboardSummarizer()
        self.finance = FinanceModule() # For handling sales and revenue
        self.employees = EmployeeManagement()
        self.inventory = InventoryManagement()
        self.logger = Logger()

    """
    These functions essentially validate the user info and then return the requested information if the user is authenticated.    
    The returned dict from all functions will then get sent back to the user in Server.py.
    The repetition can and probably should get reduced as well.
    """
    def request_dashboard(self, cookies: dict) -> dict:
        """
        Parameters: 
            - cookies: the cookies from the GET request, forwarded from Server.py
        Returns:
            - A dict containing the data that will the be sent back to the user from Server.py
        """
        session_token = cookies["token"]
        email = cookies["email"]
        password = cookies["password"]
        if self.auth_handler.is_valid_user(session_token, email, password):
            dashboard_contents = self.dashboard.summarize_reports(email, password)
            return {"status_code": 200, "message": "Successfully retrieved dashboard", "data": dashboard_contents}
        else:
            return {"status_code": 401, "message": "Session timeout/invalid email/invalid password", "data": {}}

    def request_sales(self, cookies: dict) -> dict:
        session_token = cookies["token"]
        email = cookies["email"]
        password = cookies["password"]
        if self.auth_handler.is_valid_user(session_token, email, password):
            ...
    
    def request_revenue(self, cookies: dict) -> dict:
        session_token = cookies["token"]
        email = cookies["email"]
        password = cookies["password"]
        if self.auth_handler.is_valid_user(session_token, email, password):
            ...

    def request_inventory(self, cookies: dict) -> dict:
        session_token = cookies["token"]
        email = cookies["email"]
        password = cookies["password"]
        if self.auth_handler.is_valid_user(session_token, email, password):
            ...

    def request_inventory_order(self, cookies: dict) -> dict:
        session_token = cookies["token"]
        email = cookies["email"]
        password = cookies["password"]
        if self.auth_handler.is_valid_user(session_token, email, password):
            ...
    
    def request_employees(self, cookies: dict) -> dict:
        session_token = cookies["token"]
        email = cookies["email"]
        password = cookies["password"]
        if self.auth_handler.is_valid_user(session_token, email, password):
            ...
    
