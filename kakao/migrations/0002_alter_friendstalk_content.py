# Generated by Django 3.2 on 2021-05-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kakao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendstalk',
            name='content',
            field=models.TextField(max_length=1000),
        ),
    ]