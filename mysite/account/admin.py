# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Classroom, Schedule, Campus, Building, Room 

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):    
    list_display = ('id','ROOM_ID','ROOM_NAME','BUILDING','TYPE','CAMPUS',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):    
    list_display = ('id','JX0404ID','TERMNAME','KCMC','TEACHER_ID',
            'TEACHER_NAME','CLASS_TIME','START_TIME','CLASSROOM_NAME',\
            'CLASSROOM_ID','XQ','KS','JS','ZC1','ZC2','SJBZ','SHOWTEXT',)

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):    
    list_display = ('id','name')

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):    
    list_display = ('id','campus','name')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):    
    list_display = ('id','buildings','name')

