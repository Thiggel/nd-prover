from .helpers import Justification, parse_formula, parse_rule


def test_proof_spinner_symmetric_arith_valid(build_spinner_prefix):
    proof = build_spinner_prefix()
    target = parse_formula('1/4 = P(c)')
    proof.add_line(target, Justification(parse_rule('ARITH'), (6,)))
    assert proof.proof.seq[-1].formula == target
