from unittest.mock import patch
import pytest
from checker import main


def test_range():
    array = main(["--range", "13821428", "13821430"])
    assert array == ["0xD16bdCCAe06DFD701a59103446A17e22e9ca0eF0"]


def test_block():
    array = main(["--block", "13821429"])
    assert array == ["0xD16bdCCAe06DFD701a59103446A17e22e9ca0eF0"]


def test_none(capsys):
    array = main(["--block", "13821427"])
    assert array == []
