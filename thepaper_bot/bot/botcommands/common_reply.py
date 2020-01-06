from .decorate import send_text_message


class CommonReply():
    @staticmethod
    @send_text_message
    def unknown(url, chat_id):
        text = ("抱歉，不支持的指令 ╮(￣▽￣)╭ \n\n"
                "试试获取热点新闻: /get_day")
        return text
