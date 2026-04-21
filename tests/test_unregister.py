"""
Integration tests for the unregister endpoint.

Tests the DELETE /activities/{activity_name}/signup endpoint which removes
students from activities.
"""

import pytest


class TestDeleteUnregister:
    """Test suite for DELETE /activities/{activity_name}/signup endpoint."""
    
    def test_unregister_existing_participant_succeeds(self, client):
        """
        Test that an existing participant can be removed from an activity.
        
        AAA Pattern:
        - ARRANGE: Identify participant already registered (Chess Club)
        - ACT: Make DELETE request to unregister endpoint
        - ASSERT: Verify successful response
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Known to be registered
        expected_status = 200
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # ASSERT
        assert response.status_code == expected_status
        assert "Unregistered" in response.json()["message"]
    
    def test_unregister_removes_participant_from_list(self, client):
        """
        Test that unregister actually removes participant from the activity.
        
        AAA Pattern:
        - ARRANGE: Identify a registered participant
        - ACT: Unregister student, then fetch activities to verify
        - ASSERT: Verify participant no longer in activity list
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # ACT
        client.delete(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        
        # ASSERT
        assert email not in participants
    
    def test_unregister_updates_availability_count(self, client):
        """
        Test that unregistering increases available spots for an activity.
        
        AAA Pattern:
        - ARRANGE: Get initial availability, identify registered participant
        - ACT: Unregister participant, then fetch activities again
        - ASSERT: Verify availability increased by 1
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"
        
        response_before = client.get("/activities")
        participants_before = len(response_before.json()[activity_name]["participants"])
        max_participants = response_before.json()[activity_name]["max_participants"]
        spots_before = max_participants - participants_before
        
        # ACT
        client.delete(f"/activities/{activity_name}/signup?email={email}")
        response_after = client.get("/activities")
        participants_after = len(response_after.json()[activity_name]["participants"])
        spots_after = max_participants - participants_after
        
        # ASSERT
        assert spots_after == spots_before + 1
        assert participants_after == participants_before - 1
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """
        Test that unregistering from non-existent activity returns 404.
        
        AAA Pattern:
        - ARRANGE: Use invalid activity name
        - ACT: Make DELETE request with invalid activity
        - ASSERT: Verify 404 status and error message
        """
        # ARRANGE
        invalid_activity = "Fantasy Activity Club"
        email = "student@mergington.edu"
        expected_status = 404
        
        # ACT
        response = client.delete(
            f"/activities/{invalid_activity}/signup?email={email}"
        )
        
        # ASSERT
        assert response.status_code == expected_status
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_nonexistent_participant_returns_400(self, client):
        """
        Test that unregistering a non-registered participant returns 400 error.
        
        AAA Pattern:
        - ARRANGE: Use activity that exists but email is not registered
        - ACT: Make DELETE request for non-existent participant
        - ASSERT: Verify 400 status and error message
        """
        # ARRANGE
        activity_name = "Basketball Team"  # Empty or minimal participants
        email = "notregistered@mergington.edu"
        expected_status = 400
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # ASSERT
        assert response.status_code == expected_status
        assert "not registered" in response.json()["detail"].lower()
    
    def test_unregister_missing_email_parameter_returns_error(self, client):
        """
        Test that unregister request without email parameter fails.
        
        AAA Pattern:
        - ARRANGE: Prepare endpoint without email query parameter
        - ACT: Make DELETE request missing email
        - ASSERT: Verify request fails (422 validation error)
        """
        # ARRANGE
        activity_name = "Chess Club"
        expected_status = 422  # Unprocessable Entity (missing required parameter)
        
        # ACT
        response = client.delete(f"/activities/{activity_name}/signup")
        
        # ASSERT
        assert response.status_code == expected_status
    
    def test_unregister_does_not_affect_other_participants(self, client):
        """
        Test that removing one participant doesn't affect others in same activity.
        
        AAA Pattern:
        - ARRANGE: Get all participants before removal
        - ACT: Remove one participant
        - ASSERT: Verify other participants still exist
        """
        # ARRANGE
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        
        response_before = client.get("/activities")
        participants_before = response_before.json()[activity_name]["participants"].copy()
        other_participants = [p for p in participants_before if p != email_to_remove]
        
        # ACT
        client.delete(f"/activities/{activity_name}/signup?email={email_to_remove}")
        response_after = client.get("/activities")
        participants_after = response_after.json()[activity_name]["participants"]
        
        # ASSERT
        for participant in other_participants:
            assert participant in participants_after
    
    def test_unregister_same_participant_twice_fails_second_time(self, client):
        """
        Test that unregistering the same participant twice fails the second time.
        
        AAA Pattern:
        - ARRANGE: Identify a registered participant
        - ACT: Unregister once (succeeds), unregister again (should fail)
        - ASSERT: First succeeds (200), second fails (400)
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # ACT - First unregister (should succeed)
        response_first = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # ACT - Second unregister (should fail)
        response_second = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # ASSERT
        assert response_first.status_code == 200
        assert response_second.status_code == 400
        assert "not registered" in response_second.json()["detail"].lower()
