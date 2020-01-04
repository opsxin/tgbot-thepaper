from pip._vendor import requests
from functools import wraps


def send_text_message(func):
    """发送文本信息"""
    @wraps(func)
    def inner(*args, **kw):
        text = func(*args, **kw)
        my_params = {"chat_id": kw.get("chat_id", None), "text": text}
        try:
            requests.get(kw.get("url", None), params=my_params)
        except Exception as e:
            print(e)
    return inner


def send_md_message(func):
    """发送 Markdown 信息"""
    @wraps(func)
    def inner(*args, **kw):
        text = func(*args, **kw)
        my_params = {"chat_id": kw.get("chat_id", None),
                     "text": text, "parse_mode": "markdown"}
        try:
            requests.get(kw.get("url", None), params=my_params)
        except Exception as e:
            print(e)
    return inner


def restricted_user(chat_id):
    """只允许列表中用户访问特定命令"""
    def outer(func):
        @wraps(func)
        def inner(*args, **kw):
            from django.conf import settings
            allow_user = settings.DJANGO_BOT.get("ALLOW_USER")
            if str(chat_id) not in allow_user:
                print("不允许的用户: {}.".format(chat_id))
                return
            return func(*args, **kw)
        return inner
    return outer
