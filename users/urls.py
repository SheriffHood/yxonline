#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.urls import path, include, re_path
from users.views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from users.views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

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

    #我的课程
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),

    #我收藏的课程机构
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),

    #我收藏的教师
    path('myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),

    #我收藏的课程
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),

    #我的消息
    path( 'mymessage/', MyMessageView.as_view(), name='mymessage' ),
]
