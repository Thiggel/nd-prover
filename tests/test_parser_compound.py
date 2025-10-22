from .helpers import And, Box, Dia, Forall, Iff, Imp, Not, Or, Pred, PropVar, Var, parse_formula


def test_parser_compound():
    assert parse_formula('(A and (B or C))') == And(PropVar('A'), Or(PropVar('B'), PropVar('C')))
    assert parse_formula('¬(A→(B∧C))') == Not(Imp(PropVar('A'), And(PropVar('B'), PropVar('C'))))
    assert parse_formula('(A∧B)→(C∨¬D)') == Imp(
        And(PropVar('A'), PropVar('B')),
        Or(PropVar('C'), Not(PropVar('D'))),
    )
    assert parse_formula('∀x(Px→Qx)') == Forall(
        Var('x'),
        Imp(Pred('P', (Var('x'),)), Pred('Q', (Var('x'),))),
    )
    assert parse_formula('□(A↔¬B)') == Box(Iff(PropVar('A'), Not(PropVar('B'))))
    assert parse_formula('¬¬A') == Not(Not(PropVar('A')))
