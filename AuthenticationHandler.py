
"""
Uses:
    - DatabaseHandler
    - Logger

Called From:
    - RequestHandler

"""

import random
import string
from Logger import Logger
from DatabaseHandler import DatabaseHandler

class AuthenticationHandler:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger()

    def generate_token(self) -> str:
        """
        Returns a random 32 character string consisting of uppercase letters and digits
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32)) 

    def is_valid_user(self, session_token: str, email: str, password: str) -> bool:
        """
        Parameters:
            - session_token: the token which corresponds to the user's session
            - email: the user's email
            - password: the user's password
        Returns:
            - True: if the token corresponds to an existing user who is currently authenticated
            - False: if the token does not correspond to an authenticated user  
        """
        if self.db_handler.contains(session_token, "sessions") and self.db_handler.contains((email, password), "users"):
            return True
        return False
    
    def login(self, email: str, password: str) -> bool:
        """
        Parameters:
            - email: the email of the user to create a session for
            - password: the password of the user to create a session for
        Returns:
            - True: if the session was successfully created
            - False: if the session was not created
        """
        return self.db_handler.insert((self.generate_token(), email, password), "sessions")
    
    def logout(self, session_token: str, email: str, password: str) -> bool:
        """
        Parameters:
            - session_token: the session token of the user to remove
            - email: the email of the user to remove
            - password: the email of the user to remove
        """
        if self.db_handler.contains((email, password), "users"):
            return self.db_handler.delete(session_token, "sessions")
        
        return False