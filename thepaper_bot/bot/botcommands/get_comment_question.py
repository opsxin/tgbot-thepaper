from datetime import datetime
from .decorate import send_md_message
from django_redis import get_redis_connection


class CommentQuestion(object):
    _myredis = get_redis_connection("default")

    @classmethod
    @send_md_message
    def get_comment(cls, url, chat_id):
        text = []
        text.append(
            "*{}，以下是今日热评：*".format(
                datetime.strftime(
                    datetime.now(), "%Y 年 %m 月 %d 日")))

        source_title_length = int(cls._myredis.get("source_title_length"))
        question_length = int(cls._myredis.get("question_length"))
        topic_length = source_title_length - question_length

        title = cls._myredis.lrange("source_title", 0, topic_length)
        comment = cls._myredis.lrange("comment", 0, topic_length)
        url = cls._myredis.lrange("source_title_url", 0, topic_length)

        for i in range(0, topic_length):
            text.append(
                "{}：{}\n热评：{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                    i + 1,
                    title[i].decode("utf-8"),
                    comment[i].decode("utf-8"),
                    url[i].decode("utf-8")))
        news_timestamp = cls._myredis.get("news_time")
        news_time = datetime.fromtimestamp(
            float(news_timestamp)).strftime("%y-%m-%d %H:%M:%S")
        text.append("_新闻获取时间: {}_\n".format(news_time))
        return "\n".join(text)

    @classmethod
    @send_md_message
    def get_answer(cls, url, chat_id):
        text = []
        text.append(
            "*{}，以下是今日热门问答：*".format(
                datetime.strftime(
                    datetime.now(), "%Y 年 %m 月 %d 日")))

        source_title_length = int(cls._myredis.get("source_title_length"))
        question_length = int(cls._myredis.get("question_length"))
        topic_length = source_title_length - question_length

        if question_length != 0:
            title = cls._myredis.lrange(
                "source_title",
                topic_length,
                source_title_length)
            question = cls._myredis.lrange("question", 0, question_length)
            comment = cls._myredis.lrange(
                "comment",
                topic_length,
                source_title_length)
            url = cls._myredis.lrange(
                "source_title_url",
                topic_length,
                source_title_length)

            for i in range(0, question_length):
                text.append(
                    "{}：{}\n*Q：*{}\n*A：*{} [thepaper.cn](https://www.thepaper.cn/{})\n".format(
                        i + 1,
                        title[i].decode("utf-8"),
                        question[i].decode("utf-8"),
                        comment[i].decode("utf-8"),
                        url[i].decode("utf-8")))
            news_timestamp = cls._myredis.get("news_time")
            news_time = datetime.fromtimestamp(
                float(news_timestamp)).strftime("%y-%m-%d %H:%M:%S")
            text.append("_新闻获取时间: {}_\n".format(news_time))
            return "\n".join(text)
        else:
            return "抱歉，暂未获取到热回答。"
