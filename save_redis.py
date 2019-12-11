#!/usr/bin/python3

import re
import redis
import requests

from bs4 import BeautifulSoup


def get_paper():
    URL = "https://www.thepaper.cn/"
    html_doc = requests.get(URL).text
    # with open("thepaper.html", "w", encoding="UTF-8") as f:
    #     f.writelines(html_doc)
    # with open("thepaper.html", "r", encoding="UTF-8") as f:
    #     html_doc = f.readlines()
    # return str(html_doc)
    return html_doc


def save_news_topic(soup, myredis, selecter, name):
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
    # 问答每日不一定有 5 个
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
    pool = redis.ConnectionPool(
        host="172.17.0.2",
        port=6379,
        password="75tVW7WVa3h3Fzk$",
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

