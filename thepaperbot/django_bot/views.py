from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update
from telegram.ext import Dispatcher

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        bot_token = settings.DJANGO_BOT.get("BOT")["TOKEN"]
        bot = Bot(bot_token)

        data = json.loads(request.body.decode("utf-8"))

        dispatcher = Dispatcher(bot, None, workers=0)
        update = Update.de_json(data, bot)
        dispatcher.process_update(update)
        return HttpResponse("完成")
    else:
        return HttpResponse("错误")
