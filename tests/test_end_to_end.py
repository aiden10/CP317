def test_full_user_workflow():
    # Register User
    registration_body = {"email": "workflowuser@example.com", "password": "password123", "privilege": "employee"}
    registration_response = server.request_handler.request_registration(registration_body)
    assert registration_response["status_code"] == 200
    
    session_token = registration_response["session_token"]
    
    # Log in User
    login_body = {"email": "workflowuser@example.com", "password": "password123"}
    login_response = server.request_handler.request_login(login_body)
    assert login_response["status_code"] == 200
    
    # Access Dashboard
    dashboard_response = server.request_handler.request_dashboard(session_token)
    assert dashboard_response["status_code"] == 200
    assert "data" in dashboard_response, "Dashboard should return user data"
