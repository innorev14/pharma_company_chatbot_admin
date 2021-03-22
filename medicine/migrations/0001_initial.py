# Generated by Django 3.1.7 on 2021-03-11 14:15

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='제품명')),
                ('product_info', ckeditor.fields.RichTextField(verbose_name='제품정보')),
                ('insurance_info', ckeditor.fields.RichTextField(verbose_name='보험정보')),
                ('detail_info', ckeditor.fields.RichTextField(verbose_name='디테일 포인트')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'medicine',
                'verbose_name_plural': 'medicines',
                'ordering': ('-updated_at',),
            },
        ),
        migrations.CreateModel(
            name='MedicineTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': '태그',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedMedicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicine.medicine')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicine_taggedmedicine_items', to='medicine.medicinetag')),
            ],
            options={
                'verbose_name': 'tagged post',
                'verbose_name_plural': 'tagged posts',
            },
        ),
        migrations.AddField(
            model_name='medicine',
            name='tag',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='medicine.TaggedMedicine', to='medicine.MedicineTag', verbose_name='tag'),
        ),
    ]
