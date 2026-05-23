import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]

    # Clean up: remove the test participant
    client.delete("/activities/Chess Club/unregister", params={"email": "newstudent@mergington.edu"})

def test_signup_for_activity_already_signed_up():
    # Use an existing participant
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # Add a participant, then remove
    client.post("/activities/Art Class/signup", params={"email": "temp@mergington.edu"})
    response = client.delete("/activities/Art Class/unregister", params={"email": "temp@mergington.edu"})
    assert response.status_code == 200
    assert "Unregistered temp@mergington.edu from Art Class" in response.json()["message"]

def test_unregister_from_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_participant_not_found():
    response = client.delete("/activities/Art Class/unregister", params={"email": "notfound@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
