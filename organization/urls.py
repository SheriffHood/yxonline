#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView
from django.urls import path, re_path

app_name = 'organization'

urlpatterns = [
    path('list/', OrgView.as_view(), name='list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name='org_home'),
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='org_course'),
]
