from .helpers import FOL, Justification, Line, Rules, parse_formula


def test_rule_arith_with_citation_symmetric():
    cited_eq = parse_formula('1 - 1/3 - 5/12 = P(c)')
    conclusion = parse_formula('1/4 = P(c)')
    line = Line(8, cited_eq, Justification(Rules.PR, ()))
    assert FOL.ARITH([line], conclusion) == [conclusion]
