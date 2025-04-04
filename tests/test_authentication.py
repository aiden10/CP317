import pytest 
from AuthenticationHandler import AuthenticationHandler
from DatabaseHandler import DatabaseHandler
from Tables import Sessions

@pytest.fixture
def auth_handler():
    
    return AuthenticationHandler() 

@pytest.fixture
def db_handler():

    return DatabaseHandler()

def test_register(auth_handler, db_handler):

    result = auth_handler

    db = db_handler

    with open("tests/sample_data.txt", "r") as file:

        for lines in file:
            
            email, password, privilege = lines.strip().split(",")

            print(email)
            print(password)
            print(privilege)

            register = result.register(email, password, privilege)

            assert register != "", "Token should not be a empty string| already existing user registered again"

            # print(register) # prints out the session token returned by registering

            session = db_handler.fetch(Sessions,{"session_token": register}) # verfies if session exists
            
            assert session, "session does Not exist!"

            val1 = auth_handler.get_privilege(register) # fetches the privilege of user

            # print(val1)

            val2 = auth_handler.get_email(register) # fetches the email of user

            # print(val2)

            assert val1 != "" and val2 != "", "Session is invalid| invalid email or privilege"

            print(f"SUCCESSFUL! registration for user with {val1} privileges and email: {val2}")

    return; 


# def test_is_valid_user(db_handler):
#     db = db_handler
    

#     with open("tests/sample_data.txt", "r") as file:

#         for lines in file:
            
#             email, _, _ = lines.strip().split(",")

#             assert email != "", "invalid email cannot be empty"

#             session = db.fetch(Sessions,{"email": email}) 

#             assert session, "session does not exist, user is Not valid"

            
#             # token = session[0]["session_token"]

#             # result = db.contains(Sessions, {"session_token": token})

#             # assert result, "User is not NOT valid is not currently authenticated"

#             # print(f"user with email address: {email} is a authenticated user")

# #     return

def test_login(db_handler):
    

    return

def test_logout(db_handler):
    
    return 
