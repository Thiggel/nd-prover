from .helpers import FOL, parse_formula


def test_rule_alg_accepts_ground_identity_without_citation():
    identity = parse_formula('2/3 + 1/6 = 5/6')
    assert FOL.ALG([], identity) == [identity]
