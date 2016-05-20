from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, register


class HttpBlConfig(AppConfig):
    name = 'httpbl'


@register
def missing_settings_check(app_configs, **kwargs):
    """
    Triggers a system check error if one of the required settings is missing.
    """
    errors = []
    api_key = getattr(settings, 'HTTPBL_API_KEY', None)
    if not api_key:
        errors.append(
            Error(
                "Missing setting",
                "Please set HTTPBL_API_KEY in your settings",
                id="httpbl.E001",
            )
        )
    return errors
