from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        from . import sf_scheduler
        #if settings.SCHEDULER_AUTOSTART:                          
        sf_scheduler.start()