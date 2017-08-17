from django.apps import AppConfig


class BotsConfig(AppConfig):
    name = 'djangoprogramy.bots'
    verbose_name = "Bots"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
