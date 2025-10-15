from django.apps import AppConfig
from opentelemetry.instrumentation.auto_instrumentation import initialize
initialize()

class HelloConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hello"
