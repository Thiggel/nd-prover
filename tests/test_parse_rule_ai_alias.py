from .helpers import parse_rule


def test_parse_rule_ai_alias():
    assert parse_rule('AI').name == '∀I'
