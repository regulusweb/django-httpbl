from django.utils import unittest

from httpbl.middleware import HttpBlMiddleware


class MiddlewareTestCase(unittest.TestCase):

    def setUp(self):
        self.middleware = HttpBlMiddleware()

    def test_ban_internal_ip(self):
        ban = self.middleware.block_ip('127.0.0.1')
        self.assertEqual(ban, False)

    def test_ban_low_score(self):
        ban = self.middleware.block_ip('127.1.10.1')
        self.assertEqual(ban, False)

    def test_ban_high_score(self):
        ban = self.middleware.block_ip('127.1.80.1')
        self.assertEqual(ban, True)

    def test_ban_search_engine(self):
        ban = self.middleware.block_ip('127.1.1.0')
        self.assertEqual(ban, False)

    def test_threat_low_score(self):
        threat = self.middleware.is_threat('127.10.10.1')
        self.assertEqual(threat, False)

    def test_threat_high_score(self):
        threat = self.middleware.is_threat('127.10.75.1')
        self.assertEqual(threat, True)

    def test_threat_high_score_high_age(self):
        threat = self.middleware.is_threat('127.100.75.1')
        self.assertEqual(threat, False)

    def test_threat_low_score_high_age(self):
        threat = self.middleware.is_threat('127.100.75.1')
        self.assertEqual(threat, False)
