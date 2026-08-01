from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "StrongPassword123!",
        "display_name": "Test User"
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    assert res_data["data"]["email"] == data["email"]
    assert res_data["data"]["username"] == data["username"]
    
def test_register_duplicate_email(client: TestClient):
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "StrongPassword123!",
        "display_name": "Test User"
    }
    client.post("/api/v1/auth/register", json=data)
    
    data2 = {
        "email": "test@example.com",
        "username": "anotheruser",
        "password": "StrongPassword123!",
    }
    response = client.post("/api/v1/auth/register", json=data2)
    assert response.status_code == 409
    
def test_login_success(client: TestClient):
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "StrongPassword123!"
    }
    client.post("/api/v1/auth/register", json=data)
    
    login_data = {
        "email": "test@example.com",
        "password": "StrongPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    res_data = response.json()
    assert "access_token" in res_data["data"]
    assert "refresh_token" in response.cookies or "refresh_token" in res_data["data"]

def test_login_failure(client: TestClient):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    
def test_account_lockout(client: TestClient):
    # Register user
    client.post("/api/v1/auth/register", json={
        "email": "lockout@example.com",
        "username": "lockoutuser",
        "password": "StrongPassword123!"
    })
    
    login_data = {
        "email": "lockout@example.com",
        "password": "WrongPassword123!"
    }
    
    # 5 attempts fail
    for _ in range(5):
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        
    # 6th attempt should be 403 Forbidden because account is locked
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 403
