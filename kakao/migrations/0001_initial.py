# Generated by Django 3.2 on 2021-05-07 15:34

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendsTalk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(max_length=1000)),
                ('img_link', models.URLField(blank=True, null=True)),
                ('btn_name', models.CharField(blank=True, max_length=14, null=True)),
                ('weblink_pc', models.URLField(blank=True, null=True)),
                ('weblink_mobile', models.URLField(blank=-1, null=True)),
                ('sender', models.CharField(max_length=15)),
                ('receiver', models.TextField()),
                ('status', models.CharField(max_length=5)),
            ],
        ),
    ]
