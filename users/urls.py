#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.views import user_login
from django.urls import path

path('login/', user_login, name='login')
