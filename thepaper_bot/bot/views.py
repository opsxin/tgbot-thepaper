from django.shortcuts import render

# Create your views here.
import json
from .commands import get_comment_question, get_news_topic
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


bot_token = settings.DJANGO_BOT.get("BOT_TOKEN")
url = "https://api.telegram.org/bot{}/sendmessage".format(bot_token)


@require_http_methods(["POST"])
@csrf_exempt
def webhook(request):
    try:
        data_json = json.loads(request.body)
    except:
        return HttpResponse("失败")

    if data_json.get("message", None):
        chat_id = data_json["message"].get(
            "chat", {"id": None}).get("id")
        content = data_json["message"].get("text", None)

        if chat_id and content:
            command, *args = content.split(" ", 1)
            if command.startswith("/"):
                command = command[1:]
            gnt = get_news_topic.NewsTopic()
            gcq = get_comment_question.CommentQuestion()
            if hasattr(gnt, command):
                command = getattr(gnt, command)
                try:
                    command(url=url, chat_id=chat_id)
                except Exception as e:
                    print(e)
            elif hasattr(gcq, command):
                command = getattr(gcq, command)
                try:
                    command(url=url, chat_id=chat_id)
                except Exception as e:
                    print(e)
            else:
                return HttpResponse("失败")
    return HttpResponse("完成")
