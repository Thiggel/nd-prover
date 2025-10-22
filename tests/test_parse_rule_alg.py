from .helpers import parse_rule


def test_parse_rule_alg():
    assert parse_rule('ALG').name == 'ALG'
