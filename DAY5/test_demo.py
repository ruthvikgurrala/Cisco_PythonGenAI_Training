def test_f1() -> None:
    port = 3000
    assert port == 3000


def test_f2() -> None:
    port = 3000
    assert port > 3000  # Demonstrates a failing test assertion in pytest


def test_f3() -> None:
    app = "grafana"
    assert app == "grafana"


def test_f4() -> None:
    n = 100
    assert n < 200


def test_sample() -> None:
    status_code = 200
    assert status_code == 200


def test_sample_url() -> None:
    url = "api.com"
    assert url == "api.com"


"""
Summary by GenAI:
Demonstrates fundamental pytest test functions comparing variable states with Python's assert statement,
illustrating both passing assertions and intentional test failures.
"""