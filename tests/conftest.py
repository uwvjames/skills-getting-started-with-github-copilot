"""
Test configuration and fixtures for FastAPI application tests.

This module provides:
- TestClient fixture for making requests to the API
- State reset fixture to ensure test isolation
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(scope="function")
def client():
    """
    Fixture: Provides a TestClient instance for making HTTP requests to the API.
    
    Scope: function - A new client is created for each test function.
    """
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_activities_state():
    """
    Fixture: Resets the in-memory activities database to its initial state.
    
    This ensures test isolation by restoring the activities dict after each test.
    Without this, modifications from one test could affect subsequent tests.
    
    Scope: function - Automatically runs before and after each test function.
    autouse: True - Automatically used by all test functions without explicit declaration.
    """
    # Capture the initial state of activities (before test)
    initial_state = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy(),
        }
        for name, activity in activities.items()
    }
    
    yield  # Run the test
    
    # Restore the initial state (after test)
    activities.clear()
    activities.update(initial_state)
