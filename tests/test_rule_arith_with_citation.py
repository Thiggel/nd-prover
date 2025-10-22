from .helpers import FOL, Justification, Line, Rules, parse_formula


def test_rule_arith_with_citation():
    cited_eq = parse_formula('P(c) = 1 - 1/3 - 5/12')
    conclusion = parse_formula('P(c) = 1/4')
    line = Line(7, cited_eq, Justification(Rules.PR, ()))
    assert FOL.ARITH([line], conclusion) == [conclusion]
