# Generated by Django 3.2 on 2021-05-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kakao', '0003_alter_friendstalk_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendstalk',
            name='response_msg',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
