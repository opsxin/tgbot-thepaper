#!/usr/bin/python3

import re
import time
import redis
import requests

from bs4 import BeautifulSoup
from configparser import ConfigParser


def get_paper():
    URL = "https://www.thepaper.cn/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    }
    try:
        html_doc = requests.get(URL, headers=headers).text
    except requests.exceptions.RequestException as e:
        print(e)
        import sys
        sys.exit(1)
    else:
        return html_doc


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
    source_title = re.findall(
        re_findall,
        str(soup.select(".taq_name")))
    question = re.findall(
        re_findall,
        str(soup.select(".taq_ct")))
    comment = re.findall(
        re_findall,
        str(soup.select(".ansright_cont")))

    # 热评，问答每日为 [1, 5] 个
    source_title_length = len(soup.select(".taq_name"))
    question_length = len(soup.select(".taq_ct"))
    myredis.set("source_title_length", source_title_length)
    myredis.set("question_length", question_length)
    for i in range(0, source_title_length):
        myredis.rpush(
            "comment",
            re.sub(r"<br/>|[<<`*_>>]", "", comment[i][1]))
        if question_length != 0:
            myredis.rpush("question", question[i % question_length][1])
        myredis.rpush("source_title", source_title[i][1])
        myredis.rpush("source_title_url", source_title[i][0])


def main():
    config = ConfigParser()
    config.read("config.ini", encoding="UTF-8")

    soup = BeautifulSoup(get_paper(), "lxml")

    pool = redis.ConnectionPool(
        host=config.get("Redis", "Host"),
        port=config.get("Redis", "Port"),
        password=config.get("Redis", "Passwd"),
        decode_responses=True)
    r = redis.Redis(
        connection_pool=pool,
        decode_responses=True)
    r.flushdb()

    save_comment_answer(soup, r)
    save_news_topic(soup, r, ".list_hot", "news")
    save_news_topic(soup, r, ".topic_hot", "topic")
    r.set("news_time", time.time())


if __name__ == "__main__":
    re_findall = re.compile(r'href="(.*?)".*?>(.*?)</a>')
    main()

