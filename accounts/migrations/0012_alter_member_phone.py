# Generated by Django 3.2 on 2021-05-21 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210521_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=11, unique=True, verbose_name='전화번호'),
        ),
    ]