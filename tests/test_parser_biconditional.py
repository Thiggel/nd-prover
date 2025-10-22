from .helpers import Iff, PropVar, parse_formula


def test_parser_biconditional():
    assert parse_formula('A <-> B') == Iff(PropVar('A'), PropVar('B'))
    assert parse_formula('A↔B') == Iff(PropVar('A'), PropVar('B'))
    assert parse_formula('A≡B') == Iff(PropVar('A'), PropVar('B'))
