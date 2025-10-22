from .helpers import FOL, Justification, Line, Rules, parse_formula


def test_rule_alg_accepts_rearrangement_with_citation():
    eq_line = parse_formula('P(a) + P(b) + P(c) = 1')
    rearranged = parse_formula('P(c) = 1 - P(a) - P(b)')
    line = Line(3, eq_line, Justification(Rules.PR, ()))
    assert FOL.ALG([line], rearranged) == [rearranged]
