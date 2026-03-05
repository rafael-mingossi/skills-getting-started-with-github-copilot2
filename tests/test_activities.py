"""
Tests for GET /activities endpoint
"""
import pytest


def test_get_activities_returns_all(client):
    """Test that GET /activities returns all activities from the database"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Check that we have activities
    assert len(activities) > 0
    
    # Verify some known activities exist
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_response_structure(client):
    """Test that activity response has correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check one activity has all required fields
    activity = activities["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Verify field types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_participants_are_emails(client):
    """Test that participants list contains email addresses"""
    response = client.get("/activities")
    activities = response.json()
    
    # Get an activity with participants
    activity = activities["Chess Club"]
    
    # Verify participants are present and are strings (emails)
    assert len(activity["participants"]) > 0
    for participant in activity["participants"]:
        assert isinstance(participant, str)
        assert "@" in participant  # Basic email format check
