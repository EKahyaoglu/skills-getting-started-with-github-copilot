
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No setup needed for this test)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Clean up (Arrange-Act-Assert not strictly needed for cleanup)
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

def test_signup_for_activity_already_signed_up():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_signup_for_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # Arrange
    email = "temp@mergington.edu"
    activity = "Art Class"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

def test_unregister_from_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_participant_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Art Class"

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
