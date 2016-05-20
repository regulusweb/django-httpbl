import os

from django.conf import settings
import pytest


settings.configure(HTTPBL_API_KEY = os.environ.get('HTTPBL_API_KEY'))


@pytest.fixture
def middleware():
    from httpbl.middleware import HttpBlMiddleware
    return HttpBlMiddleware()


def test_ban_internal_ip(middleware):
    assert middleware.block_ip('127.0.0.1') == False


def test_ban_low_score(middleware):
    assert middleware.block_ip('127.1.10.1') == False


def test_ban_high_score(middleware):
    assert middleware.block_ip('127.1.80.1') == True


def test_ban_search_engine(middleware):
    assert middleware.block_ip('127.1.1.0') == False


def test_threat_low_score(middleware):
    assert middleware.is_threat('127.10.10.1') == False


def test_threat_high_score(middleware):
    assert middleware.is_threat('127.10.75.1') == True


def test_threat_high_score_high_age(middleware):
    assert middleware.is_threat('127.100.75.1') == False


def test_threat_low_score_high_age(middleware):
    assert middleware.is_threat('127.100.75.1') == False
