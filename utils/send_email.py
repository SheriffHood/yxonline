#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from random import Random
from users.models import EmailVerifyCode
from django.core.mail import send_mail, EmailMessage
from yxonline.settings import EMAIL_FROM
from django.template import loader

# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

# 发送注册邮件
def send_register_mail(email, send_type="register"):
    # 发送之前先保存到数据库，到时候查询链接是否存在

    # 实例化一个EmailVerifyCode对象
    email_record = EmailVerifyCode()
    # 生成随机的code放入链接
    if send_type == 'update_mail':
        code = random_str(4)
    else:
        code = random_str(16)
        
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定义邮件内容:
    email_title = ""
    email_body = ""

    if send_type == 'register':
        email_title = "Hood site 注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)


        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = "Hood site 重置密码链接"
        email_body = "请点击下面的链接重置你的密码: http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = "Hood site 邮箱修改验证码"
        email_body = "邮箱验证码为: {0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
