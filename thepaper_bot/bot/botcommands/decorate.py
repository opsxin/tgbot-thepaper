import logging as log

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
            log.error("BOT 发送消息失败: {}".format(e))
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
            log.error("BOT 发送消息失败: {}".format(e))
    return inner
