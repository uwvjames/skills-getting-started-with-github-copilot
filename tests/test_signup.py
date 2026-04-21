"""
Integration tests for the signup endpoint.

Tests the POST /activities/{activity_name}/signup endpoint which registers
students for activities.
"""

import pytest


class TestPostSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_with_valid_activity_and_email_succeeds(self, client):
        """
        Test that a new student can successfully sign up for an activity.
        
        AAA Pattern:
        - ARRANGE: Prepare test data (activity name and email)
        - ACT: Make POST request to signup endpoint
        - ASSERT: Verify successful response and confirmation message
        """
        # ARRANGE
        activity_name = "Basketball Team"
        email = "newstudent@mergington.edu"
        expected_status = 200
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # ASSERT
        assert response.status_code == expected_status
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """
        Test that signup actually adds the participant to the activity's list.
        
        AAA Pattern:
        - ARRANGE: Define test email
        - ACT: Sign up student, then fetch activities to verify
        - ASSERT: Verify participant appears in activities list
        """
        # ARRANGE
        activity_name = "Basketball Team"
        email = "verify@mergington.edu"
        
        # ACT
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")
        activities_data = response.json()
        
        # ASSERT
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_to_nonexistent_activity_returns_404(self, client):
        """
        Test that signing up for a non-existent activity returns 404 error.
        
        AAA Pattern:
        - ARRANGE: Use invalid activity name
        - ACT: Make POST request to signup endpoint
        - ASSERT: Verify 404 status and error message
        """
        # ARRANGE
        invalid_activity = "Non-Existent Club"
        email = "student@mergington.edu"
        expected_status = 404
        
        # ACT
        response = client.post(
            f"/activities/{invalid_activity}/signup?email={email}"
        )
        
        # ASSERT
        assert response.status_code == expected_status
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_participant_returns_400(self, client):
        """
        Test that a student cannot sign up twice for the same activity.
        
        AAA Pattern:
        - ARRANGE: Prepare email already registered (Chess Club has participants)
        - ACT: Try to sign up the same student again
        - ASSERT: Verify 400 status and duplicate error message
        """
        # ARRANGE
        activity_name = "Chess Club"
        duplicate_email = "michael@mergington.edu"  # Already registered
        expected_status = 400
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup?email={duplicate_email}"
        )
        
        # ASSERT
        assert response.status_code == expected_status
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_missing_email_parameter_returns_error(self, client):
        """
        Test that signup request without email parameter fails gracefully.
        
        AAA Pattern:
        - ARRANGE: Prepare endpoint without email query parameter
        - ACT: Make POST request missing email
        - ASSERT: Verify request fails (422 validation error)
        """
        # ARRANGE
        activity_name = "Basketball Team"
        expected_status = 422  # Unprocessable Entity (missing required parameter)
        
        # ACT
        response = client.post(f"/activities/{activity_name}/signup")
        
        # ASSERT
        assert response.status_code == expected_status
    
    def test_signup_missing_activity_name_returns_error(self, client):
        """
        Test that signup request with invalid activity path returns 404.
        
        AAA Pattern:
        - ARRANGE: Prepare endpoint path with empty activity name
        - ACT: Make POST request to invalid path
        - ASSERT: Verify 404 status
        """
        # ARRANGE
        email = "student@mergington.edu"
        expected_status = 404
        
        # ACT
        response = client.post(f"/activities//signup?email={email}")
        
        # ASSERT
        assert response.status_code == expected_status
    
    def test_signup_multiple_different_students_same_activity(self, client):
        """
        Test that multiple different students can sign up for the same activity.
        
        AAA Pattern:
        - ARRANGE: Prepare two different email addresses
        - ACT: Sign up both students to same activity
        - ASSERT: Verify both students appear in participants list
        """
        # ARRANGE
        activity_name = "Soccer Club"
        email1 = "player1@mergington.edu"
        email2 = "player2@mergington.edu"
        
        # ACT
        client.post(f"/activities/{activity_name}/signup?email={email1}")
        client.post(f"/activities/{activity_name}/signup?email={email2}")
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        
        # ASSERT
        assert email1 in participants
        assert email2 in participants
        assert len(participants) >= 2
    
    def test_signup_student_can_join_multiple_activities(self, client):
        """
        Test that a single student can sign up for multiple different activities.
        
        AAA Pattern:
        - ARRANGE: Prepare same email for two different activities
        - ACT: Sign up student to multiple activities
        - ASSERT: Verify student appears in both activities
        """
        # ARRANGE
        email = "multiactivity@mergington.edu"
        activity1 = "Soccer Club"
        activity2 = "Art Club"
        
        # ACT
        client.post(f"/activities/{activity1}/signup?email={email}")
        client.post(f"/activities/{activity2}/signup?email={email}")
        response = client.get("/activities")
        activities_data = response.json()
        
        # ASSERT
        assert email in activities_data[activity1]["participants"]
        assert email in activities_data[activity2]["participants"]
