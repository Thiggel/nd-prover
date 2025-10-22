from .helpers import And, PropVar, parse_formula


def test_parser_conjunction():
    assert parse_formula('A and B') == And(PropVar('A'), PropVar('B'))
    assert parse_formula('(A ∧ B)') == And(PropVar('A'), PropVar('B'))
    assert parse_formula('A&B') == And(PropVar('A'), PropVar('B'))
