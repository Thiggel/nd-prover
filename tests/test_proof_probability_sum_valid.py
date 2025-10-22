from .helpers import FOL, Justification, Proof, parse_formula, parse_rule


def test_probability_sum_proof_valid():
    premises = [
        parse_formula('P(a) = 2/5'),
        parse_formula('Q(a) = 3/10'),
        parse_formula('P(a) + Q(a) = R(a)'),
    ]
    conclusion = parse_formula('R(a) = 7/10')
    proof = Proof(FOL, premises, conclusion)
    proof.add_line(parse_formula('R(a) = R(a)'), Justification(parse_rule('=I'), ()))
    proof.add_line(
        parse_formula('R(a) = P(a) + Q(a)'),
        Justification(parse_rule('=E'), (3, 4)),
    )
    proof.add_line(
        parse_formula('R(a) = 2/5 + Q(a)'),
        Justification(parse_rule('=E'), (1, 5)),
    )
    proof.add_line(
        parse_formula('R(a) = 2/5 + 3/10'),
        Justification(parse_rule('=E'), (2, 6)),
    )
    proof.add_line(conclusion, Justification(parse_rule('ARITH'), (7,)))
    assert proof.is_complete()
