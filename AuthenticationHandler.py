
"""
Uses:
    - DatabaseHandler
    - Logger

Called From:
    - RequestHandler

Client should only ever store session token locally in cookies.
Email and password are only provided when logging in and registering. 
"""

import random
import string
from Logger import Logger
from DatabaseHandler import DatabaseHandler

class AuthenticationHandler:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("AuthenticationHandler")

    def generate_token(self) -> str:
        """
        Returns a random 64 character string consisting of uppercase letters and digits
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=64)) 

    def is_valid_user(self, session_token: str) -> bool:
        """
        Parameters:
            - session_token: the token which corresponds to the user's session
        Returns:
            - True: if the token corresponds to an existing user who is currently authenticated
            - False: if the token does not correspond to an authenticated user  
        """
        if len(self.db_handler.fetch(session_token, "sessions", "session_token")) > 0:
            return True
        return False
    
    def register(self, email: str, password: str, privilege: str) -> str:
        """
        Parameters:
            - email: the email of the user to create an account for
            - password: the user's password
            - privilege: the user's privilege level (owner, employee, customer)
        Returns:
            - a session_token
        """
        token = self.generate_token()
        
        # Store email and hashed password in accounts table
        create_account = self.db_handler.insert((email, hash(password), privilege), "accounts", ["email", "password_hash", "privilege"])
        create_session = self.db_handler.insert((token), "sessions", ["session_token"])
        if create_account and create_session:
            return token
        
        return ""
    
    def login(self, email: str, password: str) -> str:
        """
        Parameters:
            - email: the email of the user to check
            - password: the user's password
        Returns:
            - a session_token
        """

        # Get the account associated with the email
        account = self.db_handler.fetch((email), "accounts", "email")

        # Check the first result's hashed password against the provided one 
        if account[0][1] == hash(password):
            return self.generate_token()
        
        return ""
    
    def logout(self, session_token: str) -> bool:
        """
        Parameters:
            - session_token: the session token of the user to remove
        Returns:
            - True: if the token exists and was successfully removed
            - False if the token does not exist or something else happened preventing the removal of it
        """
        # if session token exists
        if len(self.db_handler.fetch(session_token, "sessions", "session_token")) > 0:
            return self.db_handler.delete(session_token, "sessions", "session_token") # return the delete result
        
        return False
    
    def get_email(self, session_token: str) -> str:
        """
        Parameters:
            - session_token: the session token of the user whose email we want to find
        Returns:
            - the email of the user
            - empty string if the token does not match any records
        
        Gets the email of a user by their session token
        """
        session_rows = self.db_handler.fetch(session_token, "sessions", "session_token")
        if len(session_rows) > 0:
            return session_rows[0][1] # Assuming that email is the second column
        
        return ""
    
    