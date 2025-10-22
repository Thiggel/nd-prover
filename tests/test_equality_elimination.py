from .helpers import Justification, Proof, parse_formula, parse_rule, FOL


def test_equality_elimination_with_uninterpreted_functions():
    premises = [
        parse_formula('P(a) = 1/3'),
        parse_formula('P(b) = 5/12'),
        parse_formula('P(a) + P(b) + P(c) = 1'),
    ]
    conclusion = parse_formula('P(c) = 1/4')
    proof = Proof(FOL, premises, conclusion)

    proof.add_line(
        parse_formula('P(c) = 1 - P(a) - P(b)'),
        Justification(parse_rule('ALG'), (3,)),
    )
    proof.add_line(
        parse_formula('P(c) = 1 - 1/3 - P(b)'),
        Justification(parse_rule('=E'), (1, 4)),
    )

    assert proof.proof.seq[-1].formula == parse_formula('P(c) = 1 - 1/3 - P(b)')
