#!/usr/bin/python3

import redis
import logging

from datetime import datetime
from configparser import ConfigParser
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def send_text_message(func):
    def inner(update, context):
        text = func(update, context)

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=text)
    return inner


def send_md_message(func):
    def inner(update, context):
        text = func(update, context)

        if update.message:
            chat_id = update.message.chat.id
        else:
            chat_id = update.channel_post.chat.id

        context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN)
    return inner


def get_content(name, choice, count):
    text = []
    text.append(
        "*{}，以下是{}热点：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日"),
            choice_map[choice]))

    title = myredis.lrange(name, (choice-1) * count, choice * count)
    url = myredis.lrange(
        "{}_url".format(name),
        (choice-1) * count,
        choice * count)

    for i in range(count):
        text.append(
            '{}：{} [thepaper.cn](https://www.thepaper.cn/{})'.format(
                i + 1,
                title[i],
                url[i]))
    text = "\n".join(text)

    return text


@send_text_message
def start(update, context):
    text = ("欢迎关注 ~.~ \n"
            "热点新闻：/get_news \n"
            "热点话题：/get_topics \n"
            "热点评论：/get_comment \n"
            "热点问答：/get_answer")
    return text


@send_text_message
def get_news(update, context):
    text = ("1. 今日热点新闻：/get_day \n"
            "2. 三天热点新闻：/get_days \n"
            "3. 本周热点新闻：/get_week")

    return text


@send_text_message
def get_topics(update, context):
    text = ("1. 今日热点话题：/get_day_topic \n"
            "2. 三天热点话题：/get_days_topic \n"
            "3. 本周热点话题：/get_week_topic")

    return text


@send_md_message
def get_day(update, context):
    text = get_content("news", 1, 10)

    return text


@send_md_message
def get_days(update, context):
    text = get_content("news", 2, 10)

    return text


@send_md_message
def get_week(update, context):
    text = get_content("news", 3, 10)

    return text


@send_md_message
def get_day_topic(update, context):
    text = get_content("topic", 1, 5)

    return text


@send_md_message
def get_days_topic(update, context):
    text = get_content("topic", 2, 5)

    return text


@send_md_message
def get_week_topic(update, context):
    text = get_content("topic", 3, 5)

    return text


@send_md_message
def get_comment(update, context):
    text = []
    text.append(
        "*{}，以下是今日热评：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日")))
    title = myredis.lrange("source_title", 0, 5)
    comment = myredis.lrange("comment", 0, 5)
    url = myredis.lrange("source_title_url", 0, 5)
    for i in range(0, 5):
        text.append(
            "{}：{}\n热评：{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                i + 1,
                title[i],
                comment[i],
                url[i]))
    text = "\n".join(text)

    return text


@send_md_message
def get_answer(update, context):
    text = []
    text.append(
        "*{}，以下是今日热门问答：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日")))

    answer_lenth = myredis.llen("source_title")

    title = myredis.lrange("source_title", 5, answer_lenth)
    question = myredis.lrange("question", 0, answer_lenth)
    comment = myredis.lrange("comment", 5, answer_lenth)
    url = myredis.lrange("source_title_url", 5, answer_lenth)

    for i in range(0, answer_lenth - 5):
        text.append(
            "{}：{}\n问：{}\n答：{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                i + 1,
                title[i],
                question[i],
                comment[i],
                url[i]))
    text = "\n".join(text)

    return text


def echo(update, context):
    start(update, context)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini", encoding="UTF-8")

    TOKEN = config.get("Telegram", "Token")

    choice_map = {
        1: "今日",
        2: "三天",
        3: "本周"
    }

    pool = redis.ConnectionPool(
        host=config.get("Redis", "Host"),
        port=config.get("Redis", "Port"),
        password=config.get("Redis", "Passwd"),
        decode_responses=True)
    myredis = redis.Redis(
        connection_pool=pool,
        decode_responses=True)

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get_news", get_news))
    dp.add_handler(CommandHandler("get_topics", get_topics))
    dp.add_handler(CommandHandler("get_day", get_day))
    dp.add_handler(CommandHandler("get_days", get_days))
    dp.add_handler(CommandHandler("get_week", get_week))
    dp.add_handler(CommandHandler("get_day_topic", get_day_topic))
    dp.add_handler(CommandHandler("get_days_topic", get_days_topic))
    dp.add_handler(CommandHandler("get_week_topic", get_week_topic))
    dp.add_handler(CommandHandler("get_comment", get_comment))
    dp.add_handler(CommandHandler("get_answer", get_answer))

    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.command, get_day))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

