from .helpers import Const, Pred, Var, parse_formula


def test_parser_predicate():
    assert parse_formula('Pb') == Pred('P', (Const('b'),))
    assert parse_formula('Fcdc') == Pred('F', (Const('c'), Const('d'), Const('c')))
    assert parse_formula('Kxy') == Pred('K', (Var('x'), Var('y')))
