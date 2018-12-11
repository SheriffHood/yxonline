#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.urls import path, include, re_path
from users.views import UserinfoView

app_name = 'users'

urlpatterns = [
    path('info/', UserinfoView.as_view(), name='user_info'),
]