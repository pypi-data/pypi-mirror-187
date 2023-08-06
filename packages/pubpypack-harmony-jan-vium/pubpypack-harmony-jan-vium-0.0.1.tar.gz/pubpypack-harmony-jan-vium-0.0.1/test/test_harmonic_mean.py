import sys
import pytest

from termcolor import colored

from jvnpack.harmony import main


def test_always_passes():
    assert True


@pytest.mark.parametrize(
    "inputs, expected_value",
    [
        (["1", "4", "4"], 2.0),
        (["1", "0"], 0.0),
        (["1", "a"], 0.0),
    ],
)
def test_harmony_happy_path(monkeypatch, capsys, inputs, expected_value):
    monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)

    main()

    assert capsys.readouterr().out.strip() == colored(
        expected_value,
        "red",
        "on_cyan",
        attrs=["bold"],
    )


@pytest.mark.xfail
def test_something():
    raise AssertionError()
