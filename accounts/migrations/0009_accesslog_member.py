# Generated by Django 3.2 on 2021-05-06 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210426_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, verbose_name='이름')),
                ('kakao_id', models.CharField(blank=True, max_length=70, null=True, verbose_name='카카오ID')),
                ('phone', models.CharField(max_length=11)),
                ('is_superuser', models.BooleanField(default=0, verbose_name='관리자여부')),
                ('is_active', models.BooleanField(verbose_name='활성상태')),
                ('is_staff', models.BooleanField(verbose_name='관리자여부')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.group', verbose_name='그룹이름')),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자',
            },
        ),
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intent_id', models.CharField(max_length=30, verbose_name='발화ID')),
                ('intent_name', models.CharField(max_length=30, verbose_name='발화블록명')),
                ('utterance', models.CharField(max_length=30, verbose_name='발화내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='발화일시')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.group')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.member')),
            ],
            options={
                'verbose_name': '사용기록',
            },
        ),
    ]
