# Generated by Django 2.2 on 2020-01-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagelog',
            name='name',
            field=models.CharField(default='hsin', max_length=32, verbose_name='First Name'),
        ),
    ]
