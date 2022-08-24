from django.apps import AppConfig
from django.conf import settings


class ArigongganConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arigonggan'
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import views
            views.seatChangeDisable()
            views.seatChangeActivate()
