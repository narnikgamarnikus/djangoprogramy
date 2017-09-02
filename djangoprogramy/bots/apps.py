from django.apps import AppConfig


class BotsConfig(AppConfig):
    name = 'djangoprogramy.bots'
    verbose_name = "Bots"

    def ready(self):
    	import .signals
