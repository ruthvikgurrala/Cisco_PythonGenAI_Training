from demo47 import calc


def test_calc() -> None:
    assert calc(10, 20) == 30


"""
Summary by GenAI:
Demonstrates basic unit testing in pytest by importing an application function (calc from demo47)
and validating its output against expected values using an assert statement.
"""