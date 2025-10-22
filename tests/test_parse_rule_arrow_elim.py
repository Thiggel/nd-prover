from .helpers import parse_rule


def test_parse_rule_arrow_elim():
    assert parse_rule('->E').name == '→E'
