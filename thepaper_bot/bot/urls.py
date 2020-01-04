from django.urls import path
from . import views
from django.conf import settings


webhook_prefix = settings.DJANGO_BOT.get("WEBHOOK_PREFIX")
if webhook_prefix.startswith("/"):
    webhook_prefix = webhook_prefix[1:]
if not webhook_prefix.endswith("/"):
    webhook_prefix += "/"

urlpatterns = [
    path('{}'.format(webhook_prefix), views.webhook),
]
