import pytest


@pytest.fixture
def input_data() -> int:
    return 39


def test_divisible_by_3(input_data: int) -> None:
    assert input_data % 3 == 0


def test_divisible_by_6(input_data: int) -> None:
    assert input_data % 6 == 0  # Demonstrates a failing assertion (39 is not divisible by 6)


"""
Summary by GenAI:
Demonstrates pytest fixtures (@pytest.fixture) for dependency injection, supplying test data
across multiple test functions to evaluate divisibility conditions.
"""