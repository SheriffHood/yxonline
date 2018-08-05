#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.views import LoginView
from django.urls import path

path('login/', LoginView.as_view(), name='login')
