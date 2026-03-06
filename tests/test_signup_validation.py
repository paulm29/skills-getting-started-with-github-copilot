"""Unit tests for signup validation logic using AAA pattern"""

import pytest
from src.app import activities


def test_signup_adds_participant_to_activity(client):
    """Test that signup successfully adds participant to activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@example.com"
    initial_participants = activities[activity_name]["participants"].copy()

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) + 1


def test_signup_validates_activity_exists(client):
    """Test signup validation for activity existence"""
    # Arrange
    activity_name = "Invalid Activity"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_prevents_duplicate_signup(client):
    """Test signup validation prevents duplicate signups"""
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act - Second signup with same email
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Check only one instance in participants
    assert activities[activity_name]["participants"].count(email) == 1