#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.models import UserProfile
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.db.models import Q

from users.forms import LoginForm, RegisterForm
from untils.send_email import send_register_eamil

class LoginView(View):

    def get(self, request):
        # render渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "login.html", {})

    def post(self, request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
        # POST中的usernamepassword，会对应到form中
        login_form = LoginForm(request.POST)
        #is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面值
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null说明验证成功
            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                login(request, user)
                # 跳转到首页 user request会被带回到首页
                return render(request, "index.html")
                # 验证不成功跳回登录页面
                # 没有成功说明里面的值是None，并再次跳转回主页面
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误! "})
        else:
            return render(
                request, "login.html", {
                    "login_form": login_form })


def user_login(request):
    if request.method == "POST":
        user_name = request.POST.post("username", "")
        pass_word = request.POST.post("password", "")

        user = authenticate(username= user_name, password= pass_word)

        if user is not None:
            login(request, user)
            return render(request, "index.html")
      
        else:
            return render(request, "login.html", {"msg":"wrong pwd or username"})

    elif request.method == "GET":
        return render(request, "login.html", {})

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get( Q(username=username)|Q(email=username) )
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', "")
            pass_word = request.POST.get('password', "")

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.password = pass_word

            user_profile.password = make_password(pass_word)
            user_profile.save()
            
            send_register_eamil(user_name, 'register')

            return render(request, 'login.html')
        else:
            return render(
                request, 'register.html', {
                    'register_form':register_form}
            )
