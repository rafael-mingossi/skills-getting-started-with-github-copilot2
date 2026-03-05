"""
Tests for POST /activities/{activity_name}/signup endpoint
"""
import pytest


def test_signup_success(client):
    """Test that a new participant can sign up for an activity"""
    # Get initial state
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"].copy()
    initial_count = len(initial_participants)
    
    # Sign up a new participant
    new_email = "newstudent@mergington.edu"
    response = client.post(
        f"/activities/Chess Club/signup",
        params={"email": new_email}
    )
    
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify the participant was added
    response = client.get("/activities")
    updated_participants = response.json()["Chess Club"]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert new_email in updated_participants


def test_signup_duplicate_email_rejected(client):
    """Test that duplicate signup attempts are rejected with 400"""
    # Try to sign up an already registered participant
    response = client.post(
        f"/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}  # Already in Chess Club
    )
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_activity_not_found(client):
    """Test that signing up for non-existent activity returns 404"""
    response = client.post(
        f"/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_with_special_characters_in_activity_name(client):
    """Test that activity names with special characters are handled correctly"""
    # URL-encode special characters in activity name
    import urllib.parse
    
    # Assuming Programming Class has participants, try to add to it
    email = "test.user+tag@mergington.edu"
    activity_name = "Programming Class"
    encoded_activity = urllib.parse.quote(activity_name, safe='')
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Should succeed (activity exists)
    assert response.status_code == 200


def test_signup_multiple_different_activities(client):
    """Test that a student can sign up for multiple different activities"""
    email = "multiactivity@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        f"/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        f"/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both activities have the participant
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]
