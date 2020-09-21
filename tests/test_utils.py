""" Main test module for all utils. TODO: Add more tests here"""
from utils import is_playstyle_valid


def test_is_playstyle_valid():
    """ Checks that the playstyle passed in is valid"""
    result = is_playstyle_valid("awakened")
    assert result is False

    result = is_playstyle_valid("SUCcesSION")
    assert result is True

    result = is_playstyle_valid("SUCcesSION")
    assert result is True

    result = is_playstyle_valid("awakenING")
    assert result is True

    result = is_playstyle_valid("aakenING")
    assert result is False

    result = is_playstyle_valid(None)
    assert result is False
