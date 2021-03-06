# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-02-03 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=16, null=True, verbose_name='教学楼名称')),
            ],
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=16, null=True, verbose_name='校区名称')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ROOM_ID', models.CharField(blank=True, max_length=16, null=True, verbose_name='教室ID')),
                ('ROOM_NAME', models.CharField(blank=True, max_length=16, null=True, verbose_name='教室名称')),
                ('BUILDING', models.CharField(blank=True, max_length=16, null=True, verbose_name='教学楼名称')),
                ('TYPE', models.CharField(blank=True, max_length=16, null=True, verbose_name='教室类型')),
                ('CAMPUS', models.CharField(blank=True, max_length=16, null=True, verbose_name='校区')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=16, null=True, verbose_name='教室名称')),
                ('buildings', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.Building')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JX0404ID', models.CharField(blank=True, max_length=32, null=True, verbose_name='ID号')),
                ('TERMNAME', models.CharField(blank=True, max_length=32, null=True, verbose_name='学期')),
                ('KCMC', models.CharField(blank=True, max_length=256, null=True, verbose_name='课程名称')),
                ('TEACHER_ID', models.CharField(blank=True, max_length=32, null=True, verbose_name='教师ID')),
                ('TEACHER_NAME', models.CharField(blank=True, max_length=32, null=True, verbose_name='教师姓名')),
                ('CLASS_TIME', models.CharField(blank=True, max_length=32, null=True, verbose_name='上课时间')),
                ('START_TIME', models.CharField(blank=True, max_length=32, null=True, verbose_name='课程安排')),
                ('CLASSROOM_NAME', models.CharField(blank=True, max_length=32, null=True, verbose_name='教室名称')),
                ('CLASSROOM_ID', models.CharField(blank=True, max_length=32, null=True, verbose_name='教室ID')),
                ('XQ', models.CharField(blank=True, max_length=32, null=True, verbose_name='星期')),
                ('KS', models.IntegerField(default=0, verbose_name='开始的课节')),
                ('JS', models.IntegerField(default=0, verbose_name='结束的课节')),
                ('ZC1', models.IntegerField(default=0, verbose_name='第几周开始课程')),
                ('ZC2', models.IntegerField(default=0, verbose_name='第几周结束课程')),
                ('SJBZ', models.IntegerField(default=0, verbose_name='有无课程')),
                ('SHOWTEXT', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注上课安排')),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='campus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.Campus'),
        ),
    ]
