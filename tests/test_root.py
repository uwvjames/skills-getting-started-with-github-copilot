"""
Integration tests for the root endpoint.

Tests the GET / endpoint which redirects to the static HTML index.
"""

import pytest


class TestRoot:
    """Test suite for root endpoint (GET /)."""
    
    def test_root_redirects_to_index_html(self, client):
        """
        Test that GET / redirects to /static/index.html with 307 status code.
        
        AAA Pattern:
        - ARRANGE: No setup needed, endpoint requires no parameters
        - ACT: Make GET request to root endpoint
        - ASSERT: Verify redirect status and location header
        """
        # ARRANGE
        expected_status = 307
        expected_location = "/static/index.html"
        
        # ACT
        response = client.get("/", follow_redirects=False)
        
        # ASSERT
        assert response.status_code == expected_status
        assert response.headers["location"] == expected_location
