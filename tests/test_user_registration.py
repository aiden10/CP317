import pytest
from Server import Server

@pytest.fixture
def server():
    return Server()


def test_user_registration(server):

    request_body = {"email": "newuser@example.com", "password": "password123", "privilege": "customer"}
    response = server.request_handler.request_registration(request_body)
    assert response["status_code"] == 200, "Registration should return status 200"
    assert "session_token" in response, "Response should contain a session token"
