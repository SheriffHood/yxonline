#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.urls import path, include, re_path
from users.views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView

app_name = 'users'

urlpatterns = [
    #查看个人信息
    path('info/', UserinfoView.as_view(), name='user_info'),

    #个人中心更新头像
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),

    #个人中心更新密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),

    #发送邮箱验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),

    #修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
]
