from .helpers import FOL, Justification, Proof, parse_formula, parse_rule


def test_cancel_proof_valid():
    conclusion = parse_formula('(5*2)/5 = 2')
    proof = Proof(FOL, [parse_formula('NZ(5)')], conclusion)
    proof.add_line(
        parse_formula('(5*2)/5 = 10/5'),
        Justification(parse_rule('ARITH'), ()),
    )
    proof.add_line(
        conclusion,
        Justification(parse_rule('CANCEL'), (1, 2)),
    )
    assert proof.proof.seq[-1].formula == conclusion
    assert proof.is_complete()
