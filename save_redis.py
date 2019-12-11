#!/usr/bin/python3

import re
import redis
import requests

from bs4 import BeautifulSoup
from configparser import ConfigParser


def get_paper():
    URL = "https://www.thepaper.cn/"
    return requests.get(URL).text


def save_news_topic(soup, myredis, selecter, name):
    """存储新闻和话题

    Args:
        selecter: BeautifulSoup 的 select。
            参数可以是 'id', '.class'
        name: redis 的 key 值
    """
    select_content = str(soup.select(selecter))
    contents = re.findall(re_findall, select_content)
    for content in contents:
        myredis.rpush(name, content[1])
        myredis.rpush("{}_url".format(name), content[0])


def save_comment_answer(soup, myredis):
    select_content = str(soup.select(".taq_name"))
    source_title = re.findall(re_findall, select_content)
    select_content = str(soup.select(".taq_ct"))
    question = re.findall(re_findall, select_content)
    select_content = str(soup.select(".ansright_cont"))
    comment = re.findall(re_findall, select_content)
    # 问答每日为 [1, 5] 个
    comment_length = len(soup.select(".ansright_cont"))
    question_length = len(soup.select(".taq_ct"))
    for i in range(0, comment_length):
        myredis.rpush(
            "comment",
            re.sub(r"<br/>|[<<`*_>>]", "", comment[i][1]))
        myredis.rpush("question", question[i % question_length][1])
        myredis.rpush("source_title", source_title[i][1])
        myredis.rpush("source_title_url", source_title[i][0])


def main():
    config = ConfigParser()
    config.read("config.ini", encoding="UTF-8")

    pool = redis.ConnectionPool(
        host=config.get("Redis", "Host"),
        port=config.get("Redis", "Port"),
        password=config.get("Redis", "Passwd"),
        decode_responses=True)
    r = redis.Redis(
        connection_pool=pool,
        decode_responses=True)
    r.flushall()

    soup = BeautifulSoup(get_paper(), "lxml")

    save_comment_answer(soup, r)
    save_news_topic(soup, r, ".list_hot", "news")
    save_news_topic(soup, r, ".topic_hot", "topic")


if __name__ == "__main__":
    re_findall = re.compile(r'href="(.*?)".*?>(.*?)</a>')
    main()

