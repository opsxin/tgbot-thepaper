from django.apps import AppConfig
from django.conf import settings
from telegram.ext import Updater


class DjangoBotConfig(AppConfig):
    name = 'django_bot'
    verbose_name = 'Django telegram bot'

    def ready(self):
        webhook_host = settings.DJANGO_BOT.get("WEBHOOK_HOST")
        if webhook_host.endswith("/"):
            webhook_host = webhook_host[:-1]

        webhook_prefix = settings.DJANGO_BOT.get("WEBHOOK_PREFIX")
        if webhook_prefix.startswith("/"):
            webhook_prefix = webhook_prefix[1:]
        if not webhook_prefix.endswith("/"):
            webhook_prefix += "/"

        bot_token = settings.DJANGO_BOT.get("BOT").get("TOKEN", None)

        try:
            update = Updater(bot_token)
            bot = update.bot
            print("{}/{}".format(webhook_host, webhook_prefix))
            bot.delete_webhook()
            bot.set_webhook("{}/{}".format(webhook_host, webhook_prefix))
            print(bot.get_webhook_info())
        except Exception as e:
            print(e)
