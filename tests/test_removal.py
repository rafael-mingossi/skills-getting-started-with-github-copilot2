"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint
"""
import pytest


def test_remove_success(client):
    """Test that a participant can be removed from an activity"""
    # First, add a participant
    email = "removal_test@mergington.edu"
    client.post(
        f"/activities/Chess Club/signup",
        params={"email": email}
    )
    
    # Verify they're added
    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]
    
    # Remove the participant
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )
    
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    
    # Verify they're removed
    response = client.get("/activities")
    assert email not in response.json()["Chess Club"]["participants"]


def test_remove_activity_not_found(client):
    """Test that removing from non-existent activity returns 404"""
    response = client.delete(
        f"/activities/Nonexistent Activity/participants/someone@mergington.edu"
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_not_found(client):
    """Test that removing non-existent participant returns 404"""
    response = client.delete(
        f"/activities/Chess Club/participants/notinactivity@mergington.edu"
    )
    
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_with_special_characters_in_email(client):
    """Test that email addresses with special characters are handled"""
    # Email with special characters
    email = "test.user+tag@mergington.edu"
    
    # Add the participant first
    response = client.post(
        f"/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Remove with the same email
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )
    assert response.status_code == 200


def test_remove_then_re_signup(client):
    """Test that a participant can re-sign up after being removed"""
    email = "resignup@mergington.edu"
    
    # Sign up
    response1 = client.post(
        f"/activities/Gym Class/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Remove
    response2 = client.delete(
        f"/activities/Gym Class/participants/{email}"
    )
    assert response2.status_code == 200
    
    # Re-sign up
    response3 = client.post(
        f"/activities/Gym Class/signup",
        params={"email": email}
    )
    assert response3.status_code == 200
    
    # Verify they're in the activity again
    response = client.get("/activities")
    assert email in response.json()["Gym Class"]["participants"]


def test_remove_other_participants_not_affected(client):
    """Test that removing one participant doesn't affect others"""
    email1 = "participant1@mergington.edu"
    email2 = "participant2@mergington.edu"
    
    # Add two participants
    client.post(f"/activities/Debate Team/signup", params={"email": email1})
    client.post(f"/activities/Debate Team/signup", params={"email": email2})
    
    # Remove the first one
    response = client.delete(f"/activities/Debate Team/participants/{email1}")
    assert response.status_code == 200
    
    # Verify first is removed but second is still there
    response = client.get("/activities")
    activities = response.json()
    assert email1 not in activities["Debate Team"]["participants"]
    assert email2 in activities["Debate Team"]["participants"]
