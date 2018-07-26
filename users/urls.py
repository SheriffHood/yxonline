#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.views import login
from django.urls import path

path('login/', login, name='login')
