from django.conf import settings


settings.configure(
    SESSION_ENGINE='rdb_session.main'
)
