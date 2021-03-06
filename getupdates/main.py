#!/usr/bin/python3

import os
import sys
import redis
import logging
import subprocess
import telegram.ext

from threading import Thread
from datetime import datetime, time
from configparser import ConfigParser
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def send_text_message(func):
    """发送文本信息"""
    def inner(update, context):
        text = func(update, context)

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=text)
    return inner


def send_md_message(func):
    """发送 Markdown 信息"""
    def inner(update, context):
        text = func(update, context)

        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            parse_mode=ParseMode.MARKDOWN)
    return inner


def send_channel_message(func):
    """发送 Markdown 信息到 Channel"""
    def inner(context):
        text = func(context)

        context.bot.send_message(
            chat_id="@thepapercn",
            text=text,
            parse_mode=ParseMode.MARKDOWN)
    return inner


def restricted_user(func):
    """只允许列表中用户访问特定命令"""
    def inner(update, context):
        user_id = update.effective_user.id
        if str(user_id) not in ALLOW_USER_LIST:
            print("不允许的用户: {}.".format(user_id))
            return
        return func(update, context)
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
            '{}：{} \n[thepaper.cn](https://www.thepaper.cn/{})\n'.format(
                i + 1,
                title[i],
                url[i]))
    news_timestamp = myredis.get("news_time")
    news_time = datetime.fromtimestamp(
        float(news_timestamp)).strftime("%y-%m-%d %H:%M:%S")
    text.append("_新闻获取时间: {}_\n".format(news_time))
    return "\n".join(text)


def restart_bot():
    print("重启 Bot...")
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


@restricted_user
@send_text_message
def reload_news(update, context):
    print("开始获取最新数据")
    s = subprocess.run(
        'bash /root/Python/get_news.sh',
        shell=True,
        executable="/bin/bash")
    if s.returncode == 0:
        return "获取完成。"
    else:
        return "获取失败，请重试。"


@send_channel_message
def channel_daily(context: telegram.ext.CallbackContext):
    return get_content("news", 1, 10)


@restricted_user
def restart(update, context):
    Thread(target=restart_bot).start()


@send_text_message
def start(update, context):
    text = ("欢迎关注 o(*≧▽≦)ツ \n"
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
    return get_content("news", 1, 10)


@send_md_message
def get_days(update, context):
    return get_content("news", 2, 10)


@send_md_message
def get_week(update, context):
    return get_content("news", 3, 10)


@send_md_message
def get_day_topic(update, context):
    return get_content("topic", 1, 5)


@send_md_message
def get_days_topic(update, context):
    return get_content("topic", 2, 5)


@send_md_message
def get_week_topic(update, context):
    return get_content("topic", 3, 5)


@send_md_message
def get_comment(update, context):
    text = []
    text.append(
        "*{}，以下是今日热评：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日")))

    source_title_length = int(myredis.get("source_title_length"))
    question_length = int(myredis.get("question_length"))
    topic_length = source_title_length - question_length

    title = myredis.lrange("source_title", 0, topic_length)
    comment = myredis.lrange("comment", 0, topic_length)
    url = myredis.lrange("source_title_url", 0, topic_length)

    for i in range(0, topic_length):
        text.append(
            "{}：{}\n热评：{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                i + 1,
                title[i],
                comment[i],
                url[i]))
    news_timestamp = myredis.get("news_time")
    news_time = datetime.fromtimestamp(
        float(news_timestamp)).strftime("%y-%m-%d %H:%M:%S")
    text.append("_新闻获取时间: {}_\n".format(news_time))
    return "\n".join(text)


@send_md_message
def get_answer(update, context):
    text = []
    text.append(
        "*{}，以下是今日热门问答：*".format(
            datetime.strftime(
                datetime.now(), "%Y 年 %m 月 %d 日")))

    source_title_length = int(myredis.get("source_title_length"))
    question_length = int(myredis.get("question_length"))
    topic_length = source_title_length - question_length

    if question_length != 0:
        title = myredis.lrange(
            "source_title",
            topic_length,
            source_title_length)
        question = myredis.lrange("question", 0, question_length)
        comment = myredis.lrange(
            "comment",
            topic_length,
            source_title_length)
        url = myredis.lrange(
            "source_title_url",
            topic_length,
            source_title_length)

        for i in range(0, question_length):
            text.append(
                "{}：{}\n*Q：*{}\n*A：*{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                    i + 1,
                    title[i],
                    question[i],
                    comment[i],
                    url[i]))
        news_timestamp = myredis.get("news_time")
        news_time = datetime.fromtimestamp(
            float(news_timestamp)).strftime("%y-%m-%d %H:%M:%S")
        text.append("_新闻获取时间: {}_\n".format(news_time))
        return "\n".join(text)
    else:
        return "抱歉，暂未获取到热回答。"


@send_text_message
def unknown(update, context):
    return "抱歉，不支持的指令 ╮(￣▽￣)╭"


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini", encoding="UTF-8")

    TOKEN = config.get("Telegram", "Token")

    ALLOW_USER_LIST = config.get("Telegram", "Allow_User")

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
    job = updater.job_queue

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
    dp.add_handler(CommandHandler("rb", restart))
    dp.add_handler(CommandHandler("rn", reload_news))

    dp.add_handler(MessageHandler(
        Filters.text | Filters.command,
        unknown))

    dp.add_error_handler(error)

    job_daily = job.run_daily(channel_daily, time(8))
    job_daily_2 = job.run_daily(channel_daily, time(20))

    updater.start_polling()
    updater.idle()

