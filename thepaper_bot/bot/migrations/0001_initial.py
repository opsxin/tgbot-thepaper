# Generated by Django 2.2 on 2020-01-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=15, verbose_name='用户 id')),
                ('username', models.CharField(blank=True, max_length=32, null=True, verbose_name='用户名')),
                ('text', models.CharField(blank=True, max_length=128, null=True, verbose_name='文本消息')),
                ('json_text', models.TextField(verbose_name='原始请求数据')),
                ('query_time', models.DateTimeField(auto_now_add=True, verbose_name='查询时间')),
            ],
            options={
                'verbose_name': '查询日志',
                'verbose_name_plural': '查询日志',
            },
        ),
    ]
