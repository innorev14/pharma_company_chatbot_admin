# Generated by Django 3.2 on 2021-06-09 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210609_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='affiliation',
            field=models.CharField(choices=[('직영', '직영'), ('대행점', '대행점')], max_length=5, verbose_name='소속'),
        ),
    ]
