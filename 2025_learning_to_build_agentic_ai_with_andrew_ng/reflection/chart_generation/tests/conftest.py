"""
Pytest configuration and fixtures for the chart generation agent tests.
"""

import pytest
import sys
from tests.mocks.adk_mocks import setup_adk_mocks, teardown_adk_mocks


def pytest_configure(config):
    """Configure pytest with ADK mocks for unit tests only."""
    # Only set up mocks if not running e2e tests
    if not config.getoption("--e2e", default=False):
        setup_adk_mocks()


def pytest_unconfigure(config):
    """Clean up after tests."""
    # Clean up ADK mocks after all tests
    teardown_adk_mocks()


@pytest.fixture(autouse=True)
def setup_test_environment(request):
    """Set up test environment for each test."""
    # Only set up mocks for unit tests, not e2e tests
    if not request.node.get_closest_marker("e2e"):
        setup_adk_mocks()
    yield
    # Cleanup is handled by pytest_unconfigure
