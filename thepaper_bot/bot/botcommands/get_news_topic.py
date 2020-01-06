from datetime import datetime
from .decorate import send_md_message
from django_redis import get_redis_connection


class NewsTopic(object):
    choice_map = {
        1: "今日",
        2: "三天",
        3: "本周"
    }
    _myredis = get_redis_connection("default")

    @classmethod
    def get_content(cls, name, choice, count):
        text = []
        text.append(
            "*{}，以下是{}热点：*".format(
                datetime.strftime(
                    datetime.now(), "%Y 年 %m 月 %d 日"),
                cls.choice_map[choice]))

        title = cls._myredis.lrange(name, (choice-1) * count, choice * count)
        url = cls._myredis.lrange(
            "{}_url".format(name),
            (choice-1) * count,
            choice * count)

        for i in range(count):
            text.append(
                '{}：{} \n[thepaper.cn](https://www.thepaper.cn/{})\n'.format(
                    i + 1,
                    title[i].decode("utf-8"),
                    url[i].decode("utf-8")))
        news_timestamp = cls._myredis.get("news_time")
        news_time = datetime.fromtimestamp(
            float(news_timestamp)).strftime("%y-%m-%d %H:%M:%S")
        text.append("_新闻获取时间: {}_\n".format(news_time))
        return "\n".join(text)

    @classmethod
    @send_md_message
    def get_day(cls, url, chat_id):
        return cls.get_content("news", 1, 10)

    @classmethod
    @send_md_message
    def get_days(cls, url, chat_id):
        return cls.get_content("news", 2, 10)

    @classmethod
    @send_md_message
    def get_week(cls, url, chat_id):
        return cls.get_content("news", 3, 10)

    @classmethod
    @send_md_message
    def get_day_topic(cls, url, chat_id):
        return cls.get_content("topic", 1, 5)

    @classmethod
    @send_md_message
    def get_days_topic(cls, url, chat_id):
        return cls.get_content("topic", 2, 5)

    @classmethod
    @send_md_message
    def get_week_topic(cls, url, chat_id):
        return cls.get_content("topic", 3, 5)
