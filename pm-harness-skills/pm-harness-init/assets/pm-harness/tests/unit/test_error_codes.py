"""Smoke tests for centralized error codes."""

from app.core import error_codes as ec


def test_success_code_is_zero() -> None:
    assert ec.SUCCESS == 0


def test_auth_codes_in_2xxxx_range() -> None:
    assert 20000 <= ec.UNAUTHORIZED < 30000
    assert 20000 <= ec.INVALID_CREDENTIALS < 30000


def test_parameter_codes_in_4xxxx_range() -> None:
    assert 40000 <= ec.INVALID_PARAMETER < 50000
