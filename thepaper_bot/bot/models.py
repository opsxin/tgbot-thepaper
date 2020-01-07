from django.db import models

# Create your models here.


class MessageLog(models.Model):
    chat_id = models.CharField("用户 id", max_length=15)
    name = models.CharField("First Name", max_length=32, default="hsin")
    username = models.CharField("用户名", max_length=32, null=True, blank=True)
    text = models.CharField("文本消息", max_length=128, null=True, blank=True)
    json_text = models.TextField(verbose_name="原始请求数据")
    query_time = models.DateTimeField(auto_now_add=True, verbose_name="查询时间")

    def __str__(self):
        return self.username if self.username else self.name

    class Meta:
        verbose_name = "查询日志"
        verbose_name_plural = verbose_name
