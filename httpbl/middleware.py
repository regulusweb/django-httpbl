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

    def is_threat(self, ip):
        logger.debug('Checking {}'.format(ip))
        cache_key = 'httpbl_{}'.format(ip)
        result = cache.get(cache_key)

        if result is None:
            ip_parts = ip.split('.')
            ip_parts.reverse()
            query = '{}.{}.{}'.format(settings.HTTPBL_API_KEY, '.'.join(ip_parts), self.HTTPBL_DOMAIN)

            try:
                result = socket.gethostbyname(query)
                bits = result.split('.')
                if not bits[0] == '127':
                    # First octet should always be 127... something went wrong
                    return False

                age = int(bits[1])
                score = int(bits[2])
                visitor_type = int(bits[3])

                # Visitor is not a search engine, malicious activity recorded
                # in the last 30 days, threat score of > 35
                result = (visitor_type > 0 and age < self.max_age and score > self.min_score)
            except socket.gaierror:
                result = False

            cache.set(cache_key, 86400)

        return result


    def process_request(self, request):
        if settings.DEBUG:
            return None

        ip = request.META.get('REMOTE_ADDR', None)

        if ip and self.is_threat(ip):
            logger.info('{} blocked'.format(ip))
            return HttpResponseForbidden()

        return None
