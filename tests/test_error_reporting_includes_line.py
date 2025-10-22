import pytest

from .helpers import FOL, Justification, JustificationError, Proof, parse_formula, parse_rule


def test_error_messages_include_line_number_and_formula(spinner_premises, spinner_conclusion):
    proof = Proof(FOL, spinner_premises, spinner_conclusion)
    with pytest.raises(JustificationError) as ctx:
        proof.add_line(
            parse_formula('P(c) = 1 - P(a) - P(b)'),
            Justification(parse_rule('ALG'), (1, 2)),
        )
    message = str(ctx.value)
    expected_formula = str(parse_formula('P(c) = 1 - P(a) - P(b)'))
    assert message.startswith('Line 4:')
    assert expected_formula in message
