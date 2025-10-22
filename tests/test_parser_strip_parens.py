from .helpers import And, PropVar, parse_formula


def test_parser_strip_parens():
    assert parse_formula('(((A)))') == PropVar('A')
    assert parse_formula('((A∧B))') == And(PropVar('A'), PropVar('B'))
