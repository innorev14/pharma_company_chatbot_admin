# Generated by Django 3.1.7 on 2021-04-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210426_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='kakao_id',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='카카오ID'),
        ),
    ]
