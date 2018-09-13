#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from courses.views import CourseListView
from django.urls import path, re_path

app_name = 'course'

urlpatterns = [
    path('list/', CourseListView.as_view(), name='course_list'),
]
