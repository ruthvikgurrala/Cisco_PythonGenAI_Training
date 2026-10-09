import pytest
import requests


@pytest.fixture
def get_url() -> int:
    url = "https://www.google.com"
    response = requests.get(url)
    return response.status_code


def test_get_operation(get_url: int) -> None:
    assert get_url == 200


"""
Summary by GenAI:
Demonstrates API testing with pytest using a fixture (@pytest.fixture) that executes an HTTP GET request
via requests and injects the resulting status code into a test assertion.
"""