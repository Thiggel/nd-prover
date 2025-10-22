from .helpers import PropVar, parse_formula


def test_parser_propvar():
    assert parse_formula('A') == PropVar('A')
    assert parse_formula('X') == PropVar('X')
