#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from organization.views import OrgView
from django.urls import path, re_path

app_name = 'organization'

urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list')
]
