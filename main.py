#!/usr/bin/python3

import re
import logging

from bs4 import BeautifulSoup
from datetime import datetime
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = ""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# 因为格式都相似，所以只需要一个
re_news = r'href="(.*?)".*>(.*?)</a>'
news_match = re.compile(re_news)


# def get_content():
#     with open("thepaper.html", "r", encoding="UTF-8") as f:
#         soup = BeautifulSoup(f, "lxml")
#         # 热新闻
#         newstop = str(soup.select(".list_hot"))
#         hotnews = re.findall(news_match, newstop)
#         # 热话题
#         topictop = str(soup.select(".topic_hot"))
#         hottopic = re.findall(news_match, topictop)
#         # 热评论和热问答
#         news_title = str(soup.select(".taq_name"))
#         original_news = re.findall(news_match, news_title)
#         contenttop = str(soup.select(".ansright_cont"))
#         content = re.findall(news_match, contenttop)
#     return hotnews, hottopic, original_news, content


def get_day(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热新闻
        newstop = str(soup.select(".list_hot"))
        hotnews = re.findall(news_match, newstop)

    text.append(
        "今天日期是：*%s*，以下是今日热点新闻："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(10):
        text.append("{}：{} [thepaper.cn](www.thepaper.cn/{})".format(
            i % 10+1, hotnews[i][1], hotnews[i][0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_days(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热新闻
        newstop = str(soup.select(".list_hot"))
        hotnews = re.findall(news_match, newstop)

    text.append(
        "今天日期是：*%s*，以下是三天热点新闻："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(10, 20):
        text.append("{}：{} [thepaper.cn](www.thepaper.cn/{})".format(
            i % 10+1, hotnews[i][1], hotnews[i][0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_week(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热新闻
        newstop = str(soup.select(".list_hot"))
        hotnews = re.findall(news_match, newstop)

    text.append(
        "今天日期是：*%s*，以下是这周热点新闻："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(20, 30):
        text.append("{}：{} [thepaper.cn](www.thepaper.cn/{})".format(
            i % 10+1, hotnews[i][1], hotnews[i][0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_day_topic(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热话题
        topictop = str(soup.select(".topic_hot"))
        hottopic = re.findall(news_match, topictop)

    text.append(
        "今天日期是：*%s*，以下是今日热点话题："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(5):
        text.append("{}：{} [thepaper.cn](www.thepaper.cn/{})".format(
            i % 5+1, hottopic[i][1], hottopic[i][0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_days_topic(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热话题
        topictop = str(soup.select(".topic_hot"))
        hottopic = re.findall(news_match, topictop)

    text.append(
        "今天日期是：*%s*，以下是三天热点话题："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(5, 10):
        text.append("{}：{} [thepaper.cn](www.thepaper.cn/{})".format(
            i % 5+1, hottopic[i][1], hottopic[i][0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def get_week_topic(update, context):
    text = []
    with open("thepaper.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f, "lxml")
        # 热话题
        topictop = str(soup.select(".topic_hot"))
        hottopic = re.findall(news_match, topictop)

    text.append(
        "今天日期是：*%s*，以下是这周热点话题："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(10, 15):
        text.append("{}：{} [thepaper.cn](www.thepaper.cn/{})".format(
            i % 5+1, hottopic[i][1], hottopic[i][0]))
    text = "\n".join(text)

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
        text.append("{}：{}\n{}[thepaper.cn](www.thepaper.cn/{})".format(
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
        # 热评论
        news_title = str(soup.select(".taq_name"))
        original_news = re.findall(news_match, news_title)
        contenttop = str(soup.select(".ansright_cont"))
        content = re.findall(news_match, contenttop)
    text.append(
        "今天日期是：*%s*，以下是今日热点问答："
        % datetime.strftime(datetime.now(), "%Y-%m-%d"))
    for i in range(5, 10):
        text.append("{}：{}\n{}[thepaper.cn](www.thepaper.cn/{})".format(
            i % 5 + 1,
            original_news[i][1],
            content[i][1],
            original_news[i][0]))
    text = "\n".join(text)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("get_day", get_day))
    dp.add_handler(CommandHandler("get_days", get_days))
    dp.add_handler(CommandHandler("get_week", get_week))
    dp.add_handler(CommandHandler("get_day_topic", get_day_topic))
    dp.add_handler(CommandHandler("get_days_topic", get_days_topic))
    dp.add_handler(CommandHandler("get_week_topic", get_week_topic))
    dp.add_handler(CommandHandler("get_comment", get_comment))
    dp.add_handler(CommandHandler("get_answer", get_answer))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
