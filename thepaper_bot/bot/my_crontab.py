import time

from bs4 import BeautifulSoup
from .botcommands import get_news_topic
from .crontab_depend import save_news_depend
from django.conf import settings
from django_redis import get_redis_connection


def send_news_to_channel():
    """发送最新新闻到频道
    每天 8 及 20 点
    """
    bot_token = settings.DJANGO_BOT.get("BOT_TOKEN")
    url = "https://api.telegram.org/bot{}/sendmessage".format(bot_token)
    chat_id = "@thepapercn"
    gnt = get_news_topic.NewsTopic()
    cmd = getattr(gnt, "get_day", None)
    if cmd:
        cmd(url=url, chat_id=chat_id)


def save_news():
    soup = BeautifulSoup(save_news_depend.get_paper(), "lxml")

    r = get_redis_connection("default")
    r.flushdb()

    save_news_depend.save_comment_answer(soup, r)
    save_news_depend.save_news_topic(soup, r, ".list_hot", "news")
    save_news_depend.save_news_topic(soup, r, ".topic_hot", "topic")
    r.set("news_time", time.time())
