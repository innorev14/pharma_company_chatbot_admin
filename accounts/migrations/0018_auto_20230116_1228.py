# Generated by Django 3.2 on 2023-01-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20210609_1227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': '관리자', 'verbose_name_plural': '관리자'},
        ),
        migrations.AddField(
            model_name='member',
            name='representative',
            field=models.CharField(choices=[('직영', '직영'), ('대표', '대표'), ('딜러', '딜러')], default='대표', max_length=5, verbose_name='대표'),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together={('main_group', 'name')},
        ),
    ]