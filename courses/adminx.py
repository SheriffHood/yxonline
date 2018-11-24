#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import xadmin
from courses.models import Course, CourseResource, Video, Lesson

class CourseAdmin(object):
    list_dispay = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']

class LessonAdmin(object):
    list_dispay = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']

class VideoAdmin(object):
    list_dispay = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name']

class CourseResourceAdmin(object):
    list_dispay = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name','name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
