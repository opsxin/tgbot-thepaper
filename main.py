#!/usr/bin/python3

import redis
import logging

from datetime import datetime
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_content(name, choice, count):
    text = []
    text.append(
        "*{}，以下是{}热点：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日"),
            choice_map[choice]))
    for i in range((choice-1) * count, choice * count):
        text.append(
            '{}：{} [thepaper.cn](https://www.thepaper.cn/{})'.format(
                i % count + 1,
                myredis.lrange(name, i, i)[0],
                myredis.lrange("{}_url".format(name), i, i)[0]))
    text = "\n".join(text)

    return text


def start(update, context):
    text = ("欢迎关注 ~.~ \n"
            "热点新闻：/get_news \n"
            "热点话题：/get_topics \n"
            "热点评论：/get_comment \n"
            "热点问答：/get_answer")

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text)


def get_news(update, context):
    text = ("1. 今日热点新闻：/get_day \n"
            "2. 三天热点新闻：/get_days \n"
            "3. 本周热点新闻：/get_week")

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text)


def get_topics(update, context):
    text = ("1. 今日热点话题：/get_day_topic \n"
            "2. 三天热点话题：/get_days_topic \n"
            "3. 本周热点话题：/get_week_topic")

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text)


def get_day(update, context):
    text = get_content("news", 1, 10)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_days(update, context):
    text = get_content("news", 2, 10)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_week(update, context):
    text = get_content("news", 3, 10)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_day_topic(update, context):
    text = get_content("topic", 1, 5)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_days_topic(update, context):
    text = get_content("topic", 2, 5)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_week_topic(update, context):
    text = get_content("topic", 3, 5)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_comment(update, context):
    text = []
    text.append(
        "*{}，以下是今日热评：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日")))
    for i in range(0, 5):
        text.append(
            "{}：{}\n热评：{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                i + 1,
                myredis.lrange("source_title", i, i)[0],
                myredis.lrange("comment", i, i)[0],
                myredis.lrange("source_title_url", i, i)[0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_answer(update, context):
    text = []
    text.append(
        "*{}，以下是今日热门问答：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日")))
    answer_lenth = myredis.llen("source_title")
    for i in range(5, answer_lenth):
        text.append(
            "{}：{}\n问：{}\n答：{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                i % 5 + 1,
                myredis.lrange("source_title", i, i)[0],
                myredis.lrange("question", i-5, i-5)[0],
                myredis.lrange("comment", i, i)[0],
                myredis.lrange("source_title_url", i, i)[0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def echo(update, context):
    start(update, context)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    TOKEN = ""
    choice_map = {
        1: "今日",
        2: "三天",
        3: "本周"
    }

    pool = redis.ConnectionPool(
        host="172.17.0.2",
        port=6379,
        password="75tVW7WVa3h3Fzk$",
        decode_responses=True)
    myredis = redis.Redis(
        connection_pool=pool,
        charset="utf-8",
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

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

