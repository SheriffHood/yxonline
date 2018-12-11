#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.urls import path, include, re_path
from users.views import UserinfoView, UploadImageView, UpdatePwdView

app_name = 'users'

urlpatterns = [
    path('info/', UserinfoView.as_view(), name='user_info'),

    path('image/upload/', UploadImageView.as_view(), name='image_upload'),

    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
]