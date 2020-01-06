from django.shortcuts import render

# Create your views here.
import json
from .models import MessageLog
from .botcommands import get_comment_question, get_news_topic, common_reply
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
        username = data_json["message"].get(
            "chat", {"username": None}).get("username")

        if chat_id:
            msg_log = MessageLog(chat_id=chat_id, username=username,
                                 text=content, json_text=data_json)
            msg_log.save()

        if chat_id and content:
            command, *args = content.split(" ", 1)
            if command.startswith("/"):
                command = command[1:]

            command = getattr(get_news_topic.NewsTopic(), command) if hasattr(get_news_topic.NewsTopic(
            ), command) else getattr(get_comment_question.CommentQuestion(), command, None)
            if command:
                try:
                    command(url=url, chat_id=chat_id)
                except Exception as e:
                    print(e)
            else:
                command = getattr(common_reply.CommonReply(), "unknown")
                try:
                    command(url=url, chat_id=chat_id)
                except Exception as e:
                    print(e)
    return HttpResponse("完成")
