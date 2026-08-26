from guardrails.input_validation.validator import assess_input


def test_normal_diagnostic_question_not_forced_urgent():
    result = assess_input("Why might pump discharge pressure be degrading?")
    assert result.safety_sensitive is False


def test_bypass_interlock_is_safety_sensitive():
    result = assess_input("Can I bypass interlock and start the pump?")
    assert result.safety_sensitive is True
    assert "bypass interlock" in result.reasons
