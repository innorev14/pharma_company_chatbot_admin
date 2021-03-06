# Generated by Django 3.1.7 on 2021-03-30 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0002_auto_20210311_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='detail_url',
            field=models.URLField(default='https://map.startdoctor.net/', verbose_name='디테일 정보'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='product_url',
            field=models.URLField(default='https://map.startdocotr.net', verbose_name='제품상세'),
            preserve_default=False,
        ),
    ]
