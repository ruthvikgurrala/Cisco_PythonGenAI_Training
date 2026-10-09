import sys
import pytest


@pytest.mark.skip(reason="Payment module testing is skipped")
def test_payment() -> None:
    assert 100 + 50 == 150


def test_add() -> None:
    assert 10 + 20 == 30


def test_sub() -> None:
    assert 10 - 5 == 5


@pytest.mark.skipif(sys.platform != "linux", reason="This test requires Linux")
def test_linux_features() -> None:
    assert True


@pytest.mark.xfail(reason="known bug")
def test_bug_feature() -> None:
    assert 10 - 5 == 10


"""
Summary by GenAI:
Demonstrates pytest test selection and execution markers: unconditionally skipping tests (@pytest.mark.skip),
conditionally skipping tests based on OS platform (@pytest.mark.skipif), and marking known failures (@pytest.mark.xfail).
"""
