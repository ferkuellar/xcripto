from app.core.state_machine import (
    get_allowed_news_status_transitions,
    is_valid_news_status_transition,
)


def test_state_machine_allows_expected_transition():
    assert is_valid_news_status_transition("detected", "registered") is True


def test_state_machine_blocks_invalid_transition():
    assert is_valid_news_status_transition("detected", "verified") is False


def test_state_machine_allows_escalation_from_non_final_status():
    assert is_valid_news_status_transition("reviewing", "escalated") is True


def test_state_machine_blocks_final_status_reopening():
    assert is_valid_news_status_transition("archived", "published") is False


def test_state_machine_reports_allowed_transitions():
    assert get_allowed_news_status_transitions("published") == {
        "distributed",
        "corrected",
        "retracted",
        "escalated",
    }
