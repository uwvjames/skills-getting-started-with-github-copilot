"""
Integration tests for the activities endpoint.

Tests the GET /activities endpoint which retrieves all available activities.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""
    
    def test_get_all_activities_returns_success(self, client):
        """
        Test that GET /activities returns HTTP 200 with all activities.
        
        AAA Pattern:
        - ARRANGE: No setup needed; test against existing activities
        - ACT: Make GET request to /activities endpoint
        - ASSERT: Verify status code and response is a dictionary
        """
        # ARRANGE
        expected_status = 200
        
        # ACT
        response = client.get("/activities")
        
        # ASSERT
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all configured activities.
        
        AAA Pattern:
        - ARRANGE: Define expected activities
        - ACT: Make GET request and retrieve response
        - ASSERT: Verify all expected activities are present
        """
        # ARRANGE
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer Club",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club"
        ]
        
        # ACT
        response = client.get("/activities")
        activities_data = response.json()
        
        # ASSERT
        for activity_name in expected_activities:
            assert activity_name in activities_data
    
    def test_activity_has_required_fields(self, client):
        """
        Test that each activity contains required fields.
        
        AAA Pattern:
        - ARRANGE: Define required fields for each activity
        - ACT: Fetch activities and check first activity structure
        - ASSERT: Verify required fields exist
        """
        # ARRANGE
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants"
        }
        
        # ACT
        response = client.get("/activities")
        activities_data = response.json()
        first_activity = next(iter(activities_data.values()))
        
        # ASSERT
        assert all(field in first_activity for field in required_fields)
    
    def test_participants_is_list(self, client):
        """
        Test that participants field is a list in all activities.
        
        AAA Pattern:
        - ARRANGE: Test against all activities
        - ACT: Fetch activities
        - ASSERT: Verify participants is a list for each activity
        """
        # ARRANGE & ACT
        response = client.get("/activities")
        activities_data = response.json()
        
        # ASSERT
        for activity_name, activity_data in activities_data.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be a list"
    
    def test_activity_with_participants_shows_registered_students(self, client):
        """
        Test that activities with existing participants display them correctly.
        
        AAA Pattern:
        - ARRANGE: Identify an activity with participants
        - ACT: Fetch activities
        - ASSERT: Verify participants list contains registered emails
        """
        # ARRANGE
        activity_with_participants = "Chess Club"  # Known to have participants
        
        # ACT
        response = client.get("/activities")
        activities_data = response.json()
        chess_club = activities_data[activity_with_participants]
        
        # ASSERT
        assert len(chess_club["participants"]) > 0
        assert isinstance(chess_club["participants"][0], str)
        assert "@" in chess_club["participants"][0]
