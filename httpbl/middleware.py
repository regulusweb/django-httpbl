import logging
import socket

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)


class HttpBlMiddleware:

    HTTPBL_DOMAIN = 'dnsbl.httpbl.org'

    def __init__(self):
        self.max_age = getattr(settings, 'HTTPBL_THREAT_AGE', 30)
        self.min_score = getattr(settings, 'HTTPBL_THREAT_SCORE', 40)
        self.cache_lifetime = getattr(settings, 'HTTPBL_CACHE_LIFETIME', 86400)

    def is_threat(self, httpbl_response):
        bits = httpbl_response.split('.')
        if not bits[0] == '127':
            # First octet should always be 127... something went wrong
            return False

        age = int(bits[1])
        score = int(bits[2])
        visitor_type = int(bits[3])

        # Visitor is not a search engine, malicious activity recorded
        # in the last 30 days, threat score of > 35
        return (visitor_type > 0 and age < self.max_age and score > self.min_score)

    def block_ip(self, ip):
        cache_key = 'httpbl_{}'.format(ip)
        result = cache.get(cache_key)

        if result is None:
            logger.debug('Checking {}'.format(ip))
            ip_parts = ip.split('.')
            # Http:BL needs the ip with the octects reversed
            ip_parts.reverse()
            query = '{}.{}.{}'.format(settings.HTTPBL_API_KEY, '.'.join(ip_parts), self.HTTPBL_DOMAIN)

            try:
                response = socket.gethostbyname(query)
            except socket.gaierror:
                result = False
            else:
                result = self.is_threat(response)

            cache.set(cache_key, result, self.cache_lifetime)

        return result

    def process_request(self, request):
        if settings.DEBUG:
            return None

        ip = request.META.get('REMOTE_ADDR', None)

        if ip and self.block_ip(ip):
            logger.info('{} blocked'.format(ip))
            return HttpResponseForbidden()

        return None
