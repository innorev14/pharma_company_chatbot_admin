# Generated by Django 3.2 on 2021-06-03 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210603_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='main_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_group', to='accounts.group'),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together={('main_group',)},
        ),
    ]
