from .helpers import FOL, parse_formula


def test_rule_arith_ground_identity():
    conclusion = parse_formula('1 - 1/3 - 5/12 = 1/4')
    assert FOL.ARITH([], conclusion) == [conclusion]
