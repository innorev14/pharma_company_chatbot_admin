# Generated by Django 3.1.7 on 2021-03-30 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0003_auto_20210330_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=45, verbose_name='제품분류')),
            ],
            options={
                'unique_together': {('category',)},
            },
        ),
        migrations.AddField(
            model_name='medicine',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='medicine.category'),
        ),
    ]
