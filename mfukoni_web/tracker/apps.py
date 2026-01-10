from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mfukoni_web.tracker'  # Use full path to support running from project root
