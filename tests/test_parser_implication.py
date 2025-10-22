from .helpers import Imp, PropVar, parse_formula


def test_parser_implication():
    assert parse_formula('A -> B') == Imp(PropVar('A'), PropVar('B'))
    assert parse_formula('A⇒B') == Imp(PropVar('A'), PropVar('B'))
    assert parse_formula('A⊃B') == Imp(PropVar('A'), PropVar('B'))
    assert parse_formula('A> B') == Imp(PropVar('A'), PropVar('B'))
    assert parse_formula('(A→B)') == Imp(PropVar('A'), PropVar('B'))
