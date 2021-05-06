# Generated by Django 3.2 on 2021-05-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_accesslog_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='활성상태'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='활성상태'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='관리자여부'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='최고관리자여부'),
        ),
    ]
