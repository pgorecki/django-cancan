from django.apps import AppConfig


class CanCanConfig(AppConfig):
    name = 'cancan'

    def ready(self):
        aaa()
        pass
