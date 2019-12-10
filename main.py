#!/usr/bin/python3

import re
import logging
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = ""

choice_map = {
    1: "今日",
    2: "三天",
    3: "本周"
}


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 因为格式都相似，所以只需要一个
re_news = r'href="(.*?)".*?>(.*?)</a>'
news_match = re.compile(re_news)


def get_paper():
    URL = "https://www.thepaper.cn/"
    r = requests.get(URL)
    with open("thepaper.html", "w") as f:
        f.writelines(r.text)
    # return r.text


def get_content(selecter, choice, count):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        select_content = str(soup.select(selecter))
        content = re.findall(news_match, select_content)

    text.append(
        "今天日期是：*{}*，以下是{}热点：".format(
            datetime.strftime(datetime.now(), "%Y-%m-%d"),
            choice_map[choice]))
    for i in range((choice-1)*count, choice*count):
        text.append(
            "{}：{} [thepaper.cn](https://www.thepaper.cn/{})".format(
                i % count+1, content[i][1], content[i][0]))
    text = "\n".join(text)

    return text


def start(update, context):
    text = ("1. 获取热点新闻：/get_news \n"
            "2. 获取热点话题：/get_topics \n"
            "3. 获取热点评论：/get_comment \n"
            "4. 获取热点问答：/get_answer")

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
    text = get_content(".list_hot", 1, 10)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_days(update, context):
    text = get_content(".list_hot", 2, 10)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_week(update, context):
    text = get_content(".list_hot", 3, 10)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_day_topic(update, context):
    text = get_content(".topic_hot", 1, 5)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_days_topic(update, context):
    text = get_content(".topic_hot", 2, 5)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_week_topic(update, context):
    text = get_content(".topic_hot", 3, 5)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_comment(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热评论
        news_title = str(soup.select(".taq_name"))
        original_news = re.findall(news_match, news_title)
        contenttop = str(soup.select(".ansright_cont"))
        content = re.findall(news_match, contenttop)
    text.append(
        "今天日期是：*%s*，以下是今日热评："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(0, 5):
        text.append(
            "{}：{}\n热评：{} [thepaper.cn](https://www.thepaper.cn/{})".format(
                i % 5 + 1,
                original_news[i][1],
                content[i][1],
                original_news[i][0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_answer(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热问答
        news_title = str(soup.select(".taq_name"))
        original_news = re.findall(news_match, news_title)
        select_question = str(soup.select(".taq_ct"))
        question = re.findall(news_match, select_question)
        select_answer = str(soup.select(".ansright_cont"))
        answer = re.findall(news_match, select_answer)
    text.append(
        "今天日期是：*%s*，以下是今日热点问答："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(5, 10):
        text.append(
            "{}：{}\n问：{}\n答：{}[thepaper.cn](https://www.thepaper.cn/{})".format(
                i % 5 + 1,
                original_news[i][1],
                question[i % 5][1],
                re.sub(r"<br/>|[<<`*_>>]", "", answer[i][1]),
                original_news[i][0]))
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
    # get_paper()

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

