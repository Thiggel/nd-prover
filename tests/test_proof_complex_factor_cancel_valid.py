from .helpers import Justification, parse_formula, parse_rule


def test_complex_factor_cancel_proof_valid(build_factor_cancel_prefix):
    proof = build_factor_cancel_prefix()
    conclusion = parse_formula('(3*a*a - 12*a)/(3*a) = a - 4')
    proof.add_line(
        parse_formula('(3*a*(a - 4))/(3*a) = a - 4'),
        Justification(parse_rule('CANCEL'), (1, 4)),
    )
    proof.add_line(
        conclusion,
        Justification(parse_rule('=E'), (2, 5)),
    )
    assert proof.is_complete()
    assert proof.proof.seq[-1].formula == conclusion
