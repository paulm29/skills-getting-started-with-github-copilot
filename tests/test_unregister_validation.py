"""Unit tests for unregister validation logic using AAA pattern"""

import pytest
from src.app import activities


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister successfully removes participant from activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "removeme@example.com"

    # First add the participant
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    initial_participants = activities[activity_name]["participants"].copy()

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) - 1


def test_unregister_validates_activity_exists(client):
    """Test unregister validation for activity existence"""
    # Arrange
    activity_name = "Invalid Activity"
    email = "test@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_validates_student_is_signed_up(client):
    """Test unregister validation requires student to be signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "notsignedup@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]