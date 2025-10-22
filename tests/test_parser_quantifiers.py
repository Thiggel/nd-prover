from .helpers import Exists, Forall, Pred, Var, parse_formula


def test_parser_quantifiers():
    assert parse_formula('forallzPz') == Forall(Var('z'), Pred('P', (Var('z'),)))
    assert parse_formula('∀sPs') == Forall(Var('s'), Pred('P', (Var('s'),)))
    assert parse_formula('existszLz') == Exists(Var('z'), Pred('L', (Var('z'),)))
    assert parse_formula('∃yPy') == Exists(Var('y'), Pred('P', (Var('y'),)))
