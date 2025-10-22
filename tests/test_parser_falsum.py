from .helpers import Falsum, parse_formula


def test_parser_falsum():
    assert parse_formula('falsum') == Falsum()
    assert parse_formula('⊥') == Falsum()
    assert parse_formula('XX') == Falsum()
    assert parse_formula('#') == Falsum()
