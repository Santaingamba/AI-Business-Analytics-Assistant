import os
import uuid
from fastapi.testclient import TestClient

def test_upload_dataset(client: TestClient, db_session):
    # Register and login to get token
    email = f"data_{uuid.uuid4()}@example.com"
    res = client.post("/api/v1/auth/register", json={
        "email": email,
        "username": f"datauser_{str(uuid.uuid4())[:8]}",
        "password": "StrongPassword123!"
    })
    
    from app.models.user import User
    from app.models.enums import Status
    user = db_session.query(User).filter(User.email == email).first()
    user.status = Status.ACTIVE
    db_session.commit()
    
    login_res = client.post("/api/v1/auth/login", json={
        "email": res.json()["data"]["email"],
        "password": "StrongPassword123!"
    })
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create dummy CSV
    csv_content = b"id,name,age,is_active\n1,Alice,30,true\n2,Bob,25,false\n"
    
    response = client.post(
        "/api/v1/datasets/upload",
        headers=headers,
        files={"file": ("test.csv", csv_content, "text/csv")},
        data={"display_name": "Test CSV", "description": "A test dataset"}
    )
    
    assert response.status_code == 200
    dataset_data = response.json()
    dataset_id = dataset_data.get("data", dataset_data)["id"]
    
    # Get details
    details_res = client.get(f"/api/v1/datasets/{dataset_id}", headers=headers)
    assert details_res.status_code == 200
    details = details_res.json().get("data", details_res.json())
    if "row_count" not in details and "display_name" not in details: # It means it was wrapped and we need to go deeper if we grabbed the wrong thing? No, if it's unwrapped, details is the object. If wrapped, details is the object.
        pass
    assert details["row_count"] == 2
    assert details["column_count"] == 4
    
    # Get preview
    preview_res = client.get(f"/api/v1/datasets/{dataset_id}/preview", headers=headers)
    assert preview_res.status_code == 200
    p_json = preview_res.json()
    preview = p_json.get("data") if "row_count" in p_json.get("data", {}) else p_json
    assert preview["row_count"] == 2
    assert preview["column_count"] == 4
    assert preview["headers"] == ["id", "name", "age", "is_active"]
    
    # Test duplicate upload
    response2 = client.post(
        "/api/v1/datasets/upload",
        headers=headers,
        files={"file": ("test2.csv", csv_content, "text/csv")}
    )
    assert response2.status_code == 409
    
    # Test soft delete
    delete_res = client.delete(f"/api/v1/datasets/{dataset_id}", headers=headers)
    assert delete_res.status_code == 200
    
    # Get after delete should fail
    get_res = client.get(f"/api/v1/datasets/{dataset_id}", headers=headers)
    assert get_res.status_code == 404
