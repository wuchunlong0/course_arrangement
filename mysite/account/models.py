# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    """教室模型"""
    ROOM_ID = models.CharField(verbose_name='教室ID', max_length=16, null=True, blank=True)
    ROOM_NAME = models.CharField(verbose_name='教室名称', max_length=16, null=True, blank=True)
    BUILDING = models.CharField(verbose_name='教学楼名称', max_length=16, null=True, blank=True)
    TYPE = models.CharField(verbose_name='教室类型', max_length=16, null=True, blank=True)
    CAMPUS = models.CharField(verbose_name='校区', max_length=16, null=True, blank=True)    
    def __str__(self):
        return self.ROOM_NAME

class Schedule(models.Model):
    """SCHEDULE """
    JX0404ID = models.CharField(verbose_name='ID号', max_length=32, null=True, blank=True)
    TERMNAME = models.CharField(verbose_name='学期', max_length=32, null=True, blank=True)
    KCMC = models.CharField(verbose_name='课程名称', max_length=256, null=True, blank=True)
    TEACHER_ID = models.CharField(verbose_name='教师ID', max_length=32, null=True, blank=True) 
    TEACHER_NAME = models.CharField(verbose_name='教师姓名', max_length=32, null=True, blank=True)    
    CLASS_TIME = models.CharField(verbose_name='上课时间', max_length=32, null=True, blank=True)    
    START_TIME = models.CharField(verbose_name='课程安排', max_length=32, null=True, blank=True)    
    CLASSROOM_NAME = models.CharField(verbose_name='教室名称', max_length=32, null=True, blank=True)    
    CLASSROOM_ID = models.CharField(verbose_name='教室ID', max_length=32, null=True, blank=True)    
    XQ = models.CharField(verbose_name='星期', max_length=32, null=True, blank=True)    
    KS = models.IntegerField(verbose_name='开始的课节', default=0)    
    JS = models.IntegerField(verbose_name='结束的课节', default=0)    
    ZC1 = models.IntegerField(verbose_name='第几周开始课程', default=0)    
    ZC2 = models.IntegerField(verbose_name='第几周结束课程', default=0)    
    SJBZ = models.IntegerField(verbose_name='有无课程', default=0)    
    SHOWTEXT = models.CharField(verbose_name='备注上课安排', max_length=256, null=True, blank=True)    
    def __str__(self):
        return self.KCMC
    
#校区
class Campus(models.Model):
    name = models.CharField(verbose_name='校区名称', max_length=16, null=True, blank=True)     
    def __str__(self):
        return self.name
#教学楼
class Building(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)
    name = models.CharField(verbose_name='教学楼名称', max_length=16, null=True, blank=True)     
    def __str__(self):
        return self.name

#教室
class Room(models.Model):
    buildings = models.ForeignKey(Building, on_delete=models.PROTECT)    
    name = models.CharField(verbose_name='教室名称', max_length=16, null=True, blank=True)     
    def __str__(self):
        return self.name
    
    
    
    