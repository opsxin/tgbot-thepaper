import re
import requests
import logging as log

from bs4 import BeautifulSoup


def get_paper():
    URL = "https://www.thepaper.cn/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    }
    try:
        html_doc = requests.get(URL, headers=headers).text
    except requests.exceptions.RequestException as e:
        log.error("请求澎湃数据失败: {}".format(e))
        import sys
        sys.exit(1)
    else:
        log.info("请求澎湃数据成功")
        return html_doc


def save_news_topic(soup, myredis, selecter, name):
    """存储新闻和话题
    Args:
        selecter: BeautifulSoup 的 select。
            参数可以是 'id', '.class'
        name: redis 的 key 值
    """
    re_findall = re.compile(r'href="(.*?)".*?>(.*?)</a>')
    select_content = str(soup.select(selecter))
    contents = re.findall(re_findall, select_content)
    for content in contents:
        myredis.rpush(name, content[1])
        myredis.rpush("{}_url".format(name), content[0])


def save_comment_answer(soup, myredis):
    re_findall = re.compile(r'href="(.*?)".*?>(.*?)</a>')
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
