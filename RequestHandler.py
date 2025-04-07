
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
        self.logger = Logger("RequestHandler")

    """
    These functions essentially validate the user info and then return the requested information if the user is authenticated.    
    The returned dict from all functions will then get sent back to the user in Server.py.
    """
    def request_registration(self, request_body: dict) -> dict:
        """
        :param request_body: the JSON data from the POST request. Should contain email, password, and user privilege
        :return response: the dict that will the be sent back to the user from Server.py
        """

        email = request_body["email"]
        password = request_body["password"]
        privilege = request_body["privilege"]
        session_token = self.auth_handler.register(email, password, privilege)
        if session_token != "":
            return {"status_code": 200, "message": "Successfully registered", "session_token": session_token}
        
        return {"status_code": 400, "message": "Failed to register", "session_token": ""}
    
    def request_login(self, request_body: dict) -> dict:
        """
        :param request_body: the JSON data from the POST request. Should contain email and password
        :return response: the dict that will the be sent back to the user from Server.py
        """

        email = request_body["email"]
        password = request_body["password"]
        session_token = self.auth_handler.login(email, password)
        if session_token != "":
            return {"status_code": 200, "message": "Successfully logged in", "session_token": session_token}
        
        return {"status_code": 400, "message": "Failed to login", "session_token": ""}
    
    def request_logout(self, cookies: dict) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will the be sent back to the user from Server.py
        """
        session_token = cookies["session_token"]
        logout_result = self.auth_handler.logout(session_token)
        if logout_result:
            return {"status_code": 200, "message": "Successfully logged out"}
        
        return {"status_code": 400, "message": "Failed to logout"}
    
    def request_dashboard(self, session_token: str) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will the be sent back to the user from Server.py
        """
        self.logger.write_log(f"Requesting dashboard with: {session_token}")
        if self.auth_handler.is_valid_user(session_token):
            email = self.auth_handler.get_email(session_token)
            dashboard_contents = self.dashboard.summarize_reports(email)

            return {"status_code": 200, "message": "Successfully retrieved dashboard", "data": dashboard_contents}

        return {"status_code": 401, "message": "Session timeout/invalid email/invalid password", "data": {}}

    def request_sales(self, session_token: str) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will the be sent back to the user from Server.py
        """
        if self.auth_handler.is_valid_user(session_token):
            email = self.auth_handler.get_email(session_token)
            sales_data = self.finance.get_sales_report(email)

            return {"status_code": 200, "message": "Successfully retrieved sales", "data": sales_data}
            
        return  {"status_code": 401, "message": "Session timeout/invalid email/invalid password", "data": {}}
    
    def request_revenue(self, session_token: str) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will the be sent back to the user from Server.py
        """
        if self.auth_handler.is_valid_user(session_token): 
            email = self.auth_handler.get_email(session_token)
            revenue = self.finance.get_revenue(email)

                
            return {"status_code": 200, "message": "Successfully retrieved revenue", "data": revenue}

        
        return {"status_code": 401, "message": "Session timeout/invalid email/invalid privileges/invalid password", "data": {}}

            

    def request_inventory(self, session_token: str) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will the be sent back to the user from Server.py
        """
        if self.auth_handler.is_valid_user(session_token):
            inventory = self.inventory.get_inventory()
            return {"status_code": 200, "message": "Successfully retrieved inventory", "data": inventory}
        
        return {"status_code": 401, "message": "Session timeout/invalid email/invalid password", "data": {}}

            

    def request_inventory_order(self, request_body: dict) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will the be sent back to the user from Server.py
        """
        session_token = request_body["session_token"]
        if self.auth_handler.is_valid_user(session_token):
            item_name = request_body["item_name"]
            quantity = request_body["quantity"]
            order = self.inventory.order_inventory(item_name, quantity)

            return {"status_code": 200, "message": "Successfully submitted a order", "data": order}
        
        return {"status_code": 401, "message": "Session timeout/invalid email/invalid password", "data": {}}
    
    def request_employees(self, session_token: str) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will the be sent back to the user from Server.py
        """
        if self.auth_handler.is_valid_user(session_token):

            employee = self.employees.get_employees()
            return {"status_code": 200, "message": "Successfully retrieved employees data", "data":employee}
        
        return {"status_code": 401, "message": "Session timeout/invalid email/invalid password", "data": {}}
     

    def request_logout(self, cookies: dict) -> dict:
        """
        :param cookies: the cookies from the GET request, forwarded from Server.py
        :return response: the dict that will be sent back to the user from Server.py
        """
        session_token = cookies.get("session_token")
        logout_result = self.auth_handler.logout(session_token)
    
        if logout_result:
            self.logger.write_log(f"User logged out: {session_token}")  # Log the logout action
            return {"status_code": 200, "message": "Successfully logged out"}
        
        self.logger.write_log(f"Failed logout attempt with session_token: {session_token}")  # Log failed attempt
        return {"status_code": 400, "message": "Failed to logout"}

    