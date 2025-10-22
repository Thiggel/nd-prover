from .helpers import Justification, parse_rule


def test_proof_spinner_valid(build_spinner_prefix, spinner_conclusion):
    proof = build_spinner_prefix()
    proof.add_line(spinner_conclusion, Justification(parse_rule('ARITH'), (6,)))
    assert proof.proof.seq[-1].formula == spinner_conclusion
    assert proof.is_complete()
