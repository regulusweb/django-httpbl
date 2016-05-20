from django.utils import unittest

from httpbl.middleware import HttpBlMiddleware


class MiddlewareTestCase(unittest.TestCase):

    def setUp(self):
        self.middleware = HttpBlMiddleware()

    def test_internal_ip(self):
        threat = self.middleware.is_threat('127.0.0.1')
        self.assertEqual(threat, False)

    def test_low_score(self):
        threat = self.middleware.is_threat('127.1.10.1')
        self.assertEqual(threat, False)

    def test_high_score(self):
        threat = self.middleware.is_threat('127.1.80.1')
        self.assertEqual(threat, True)

    def test_search_engine(self):
        threat = self.middleware.is_threat('127.1.1.0')
        self.assertEqual(threat, False)
