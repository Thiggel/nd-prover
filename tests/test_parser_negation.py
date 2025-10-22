from .helpers import Not, Pred, PropVar, Const, parse_formula


def test_parser_negation():
    assert parse_formula('~A') == Not(PropVar('A'))
    assert parse_formula('¬A') == Not(PropVar('A'))
    assert parse_formula('¬Pb') == Not(Pred('P', (Const('b'),)))
