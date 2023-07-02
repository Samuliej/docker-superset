import os
from datetime import timedelta
from cachelib.redis import RedisCache
from superset.superset_typing import CacheConfig
from celery.schedules import crontab
from flask_appbuilder.security.manager import AUTH_OAUTH

SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ALERT_REPORTS": True,
}

# Default cache for Superset objects
CACHE_CONFIG: CacheConfig = {
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=1).total_seconds()),
    # should the timeout be reset when retrieving a cached value
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_KEY_PREFIX": "superset_results",
    "CACHE_REDIS_URL": "redis://superset_cache:6379/0",
}

# Cache for datasource metadata and query results
DATA_CACHE_CONFIG: CacheConfig = {
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=1).total_seconds()),
    # should the timeout be reset when retrieving a cached value
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_KEY_PREFIX": "superset_data_cache",
    "CACHE_REDIS_URL": "redis://superset_cache:6379/0",
}

# Cache for dashboard filter state (`CACHE_TYPE` defaults to `SimpleCache` when
#  running in debug mode unless overridden)
FILTER_STATE_CACHE_CONFIG: CacheConfig = {
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=1).total_seconds()),
    # should the timeout be reset when retrieving a cached value
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_KEY_PREFIX": "superset_filter_cache",
    "CACHE_REDIS_URL": "redis://superset_cache:6379/0",
}

# Cache for explore form data state (`CACHE_TYPE` defaults to `SimpleCache` when
#  running in debug mode unless overridden)
EXPLORE_FORM_DATA_CACHE_CONFIG: CacheConfig = {
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=1).total_seconds()),
    # should the timeout be reset when retrieving a cached value
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_KEY_PREFIX": "superset_explore_form_data_cache",
    "CACHE_REDIS_URL": "redis://superset_cache:6379/0",
}


REDIS_HOST = "superset_cache"
REDIS_PORT = "6379"


class CeleryConfig:  # pylint: disable=too-few-public-methods
    broker_url = "redis://superset_cache:6379/0"
    imports = (
        "superset.sql_lab",
        "superset.tasks",
    )
    result_backend = "redis://superset_cache:6379/0"
    worker_log_level = "DEBUG"
    worker_prefetch_multiplier = 10
    task_acks_late = True
    task_annotations = {
        "sql_lab.get_sql_results": {
            "rate_limit": "100/s",
        },
        "email_reports.send": {
            "rate_limit": "1/s",
            "time_limit": 120,
            "soft_time_limit": 150,
            "ignore_result": True,
        },
    }
    beat_schedule = {
        "email_reports.schedule_hourly": {
            "task": "email_reports.schedule_hourly",
            "schedule": crontab(minute=1, hour="*"),
        },
        # https://superset.apache.org/docs/installation/alerts-reports/
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
    }


CELERY_CONFIG = CeleryConfig  # pylint: disable=invalid-name


RESULTS_BACKEND = RedisCache(
    host="superset_cache", port=6379, key_prefix="superset_results"
)


EMAIL_NOTIFICATIONS = True
SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = os.environ["SMTP_PORT"]
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
SMTP_MAIL_FROM = os.environ["SMTP_MAIL_FROM"]
SMTP_SSL_SERVER_AUTH = False

WEBDRIVER_BASEURL = "http://superset:8088/"

if os.getenv("ENABLE_OAUTH"):
    # change from AUTH_DB to AUTH_OAUTH
    AUTH_TYPE = AUTH_OAUTH

    # Will allow user self registration, allowing to create Flask users from Authorized User
    AUTH_USER_REGISTRATION = True

    # The default user self registration role
    AUTH_USER_REGISTRATION_ROLE = "Public"

    OAUTH_PROVIDERS = [
        {
            "name": "google",
            "whitelist": ["@projecttech4dev.org"],
            "token_key": "access_token",  # Name of the token in the response of access_token_url
            "icon": "fa-address-card",  # Icon for the provider
            "remote_app": {
                # "base_url": "https://www.googleapis.com/oauth2/v2/'",
                "client_id": "316034788132-a53r22euhgres5o027p220gapa8gf6gj.apps.googleusercontent.com",  # Client Id (Identify Superset application)
                "client_secret": "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",  # Secret for this Client Id (Identify Superset application)
                # "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
                "client_kwargs": {
                    # "scope": "https://www.googleapis.com/auth/userinfo.profile"
                    "scope": "email"
                },  # Scope for the Authorization
                "access_token_method": "POST",  # HTTP Method to call access_token_url
                "access_token_params": {  # Additional parameters for calls to access_token_url
                    "client_id": "316034788132-a53r22euhgres5o027p220gapa8gf6gj.apps.googleusercontent.com"
                },
                "access_token_headers": {  # Additional headers for calls to access_token_url
                    "Authorization": "Basic Base64EncodedClientIdAndSecret"
                },
                # "api_base_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "api_base_url": "https://www.googleapis.com/oauth2/v2/'",
                "access_token_url": "https://oauth2.googleapis.com/token",
                "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            },
        }
    ]

    # from .custom_security_manager import CustomSecurityManager

    # CUSTOM_SECURITY_MANAGER = CustomSecurityManager
