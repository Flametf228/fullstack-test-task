from src.domain.alerts import decide


def test_failed_is_critical():
    level, msg = decide("failed", False, None)
    assert level == "critical"
    assert msg == "File processing failed"


def test_requires_attention_is_warning():
    level, msg = decide("processed", True, "suspicious extension .exe")
    assert level == "warning"
    assert msg == "File requires attention: suspicious extension .exe"


def test_ok_is_info():
    level, msg = decide("processed", False, "no threats found")
    assert level == "info"
    assert msg == "File processed successfully"
