# Generated by Django 3.2 on 2021-05-21 14:39

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0006_auto_20210330_1646'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '제품분류', 'verbose_name_plural': '제품분류'},
        ),
        migrations.AlterModelOptions(
            name='medicine',
            options={'ordering': ('-view_count',), 'verbose_name': '의약품', 'verbose_name_plural': '의약품 리스트'},
        ),
        migrations.AlterField(
            model_name='medicine',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medicine.category', verbose_name='제품분류'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='등록일'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='detail_info',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='디테일 포인트'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='product_url',
            field=models.URLField(blank=True, null=True, verbose_name='제품상세URL'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='수정일'),
        ),
    ]
