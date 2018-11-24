# Generated by Django 2.0.7 on 2018-11-15 06:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20181115_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='章节名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程')),
            ],
            options={
                'verbose_name': '章节',
                'verbose_name_plural': '章节',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='视频名')),
                ('url', models.CharField(default='', max_length=200, verbose_name='访问地址')),
                ('learn_times', models.IntegerField(default=0, verbose_name='学习时长(分钟数)')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson', verbose_name='章节')),
            ],
            options={
                'verbose_name': '视频',
                'verbose_name_plural': '视频',
            },
        ),
    ]
