from .helpers import Or, PropVar, parse_formula


def test_parser_disjunction():
    assert parse_formula('A or B') == Or(PropVar('A'), PropVar('B'))
    assert parse_formula('(A∨B)') == Or(PropVar('A'), PropVar('B'))
