from django.conf import settings
from .botcommands import get_news_topic

bot_token = settings.DJANGO_BOT.get("BOT_TOKEN")
url = "https://api.telegram.org/bot{}/sendmessage".format(bot_token)


def send_news_to_channel():
    """发送最新新闻到频道
    每天 8 及 20 点
    """
    chat_id = "@thepapercn"
    gnt = get_news_topic.NewsTopic()
    cmd = getattr(gnt, "get_day", None)
    if cmd:
        cmd(url=url, chat_id=chat_id)
