# Generated by Django 3.2 on 2021-05-11 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kakao', '0004_friendstalk_response_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendstalk',
            name='sended_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]