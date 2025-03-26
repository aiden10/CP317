
"""
Uses:
    - DatabaseHandler
    - Logger

Called From:
    - RequestHandler

Client should only ever store session token locally in cookies.
Email and password are only provided when logging in and registering. 
"""

import bcrypt
import random
import string
from Logger import Logger
from DatabaseHandler import DatabaseHandler
from Tables import Sessions, Accounts

class AuthenticationHandler:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.logger = Logger("AuthenticationHandler")

    def generate_token(self) -> str:
        """
        :return token: a random 512 character string consisting of letters and digits
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=512)) 

    def is_valid_user(self, session_token: str) -> bool:
        """
        :param session_token: the token which corresponds to the user's session

        :return bool: 
            True: if the token corresponds to an existing user who is currently authenticated
            False: if the token does not correspond to an authenticated user  
        """
        if self.db_handler.contains(Sessions, {"session_token": session_token}):
            return True
        return False
    
    def register(self, email: str, password: str, privilege: str) -> str:
        """
        :param email: the email of the user to create an account for
        :param password: the user's password
        :param privilege: the user's privilege level (owner, employee, customer)

        :return session_token: random 512 character string consisting of letters and numbers
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()        
        password_hash = bcrypt.hashpw(password_bytes, salt)
        password_hash_str = password_hash.decode('utf-8')  # Convert bytes to string
        token = self.generate_token()
        
        # Store email and hashed password in accounts table
        create_account = self.db_handler.insert(Accounts(email=email, password_hash=password_hash_str, privilege=privilege))
        create_session = self.db_handler.insert(Sessions(session_token=token, email=email))
        if create_account and create_session:
            return token
        
        return ""
    
    def login(self, email: str, password: str) -> str:
        """
        :param email: the email of the user to check
        :param password: the user's password

        :return session_token: new session token
        """

        # Get the account associated with the email
        account = self.db_handler.fetch(Accounts, {"email": email})
        
        password_bytes = password.encode('utf-8')
        stored_hash_str = account["password_hash"]
        stored_hash_bytes = stored_hash_str.encode('utf-8')
        
        # Verify login information
        if bcrypt.checkpw(password_bytes, stored_hash_bytes):
            token = self.generate_token()
            # Update Sessions table
            insert_result = self.db_handler.insert(Sessions(session_token=token, email=email))
            if insert_result:
                self.logger.write_log(f"Logged in user: {email}")
                return token
            else:
                self.logger.write_log(f"Error adding session_token: {token} and email: {email}")
                return ""
        else:
            return ""
    
    def logout(self, session_token: str) -> bool:
        """
        :param session_token: the session token of the user to remove
        
        :return 
        - True if the token exists and was successfully removed
        - False if the token does not exist or something else happened preventing the removal of it
        """
        # if session token exists
        if self.db_handler.contains(Sessions, {"session_token": session_token}):
            return self.db_handler.delete(Sessions, {"session_token": session_token}) # return the delete result
        
        return False
    
    def get_email(self, session_token: str) -> str:
        """
        Gets the email of a user by their session token

        :param session_token: the session token of the user whose email we want to find

        :return email: the email of the user or an empty string if session doesn't exist
        """
        session_row = self.db_handler.fetch(Sessions, {"session_token": session_token})
        if session_row:
            return session_row["email"]
        
        return ""
    
    def get_privilege(self, session_token: str) -> str:
        """
        Gets the privilege of a user by their session token
        Privileges: "owner", "employee", "customer"
        :param session_token: the session token of the user whose email we want to find

        :return privilege: the privilege of the user or an empty string if session doesn't exist
        """
        session_row = self.db_handler.fetch(Sessions, {"session_token": session_token})
        if not session_row:
            return ""
        
        email = session_row["email"]
        account_row = self.db_handler.fetch(Accounts, {"email": email})
        if not account_row:
            return ""
        
        return account_row["privilege"]
        
