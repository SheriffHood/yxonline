#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.models import UserProfile, EmailVerifyCode
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.db.models import Q

from users.forms import LoginForm, RegisterForm, ModifyPwdForm, ForgetPwdForm, ActiveForm
from utils.send_email import send_register_mail
from users.models import Banner
from courses.models import Course, CourseOrg

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
            return render(request, "login.html", {"login_form": login_form })


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
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg':'User name already exists'})
            pass_word = request.POST.get('password', "")

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            user_profile.is_active = False

            user_profile.password = make_password(pass_word)
            user_profile.save()
            
            send_register_mail(user_name, 'register')

            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form':register_form})

class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyCode.objects.filter(code=active_code)
        active_form = ActiveForm(request.GET)

        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

                return render(request, 'login.html', )
        else:
            return render(request, 'register.html', {'msg': "您的激活链接无效", "active_form":active_form})

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forget_form":forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_mail(email, 'forget')

            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form':forget_form})

class ResetView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyCode.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 将email传回来
                # 只传回active_code
                return render(request, "password_reset.html", {"active_code": active_code})
        # 自己瞎输的验证码
        else:
            return render(
                request, "forgetpwd.html", {
                    "msg": "您的重置密码链接无效,请重新请求", "active_form": active_form})

class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            active_code = request.POST.get("active_code", "")
            email = request.POST.get("email", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(
                    request, "password_reset.html", {
                        "email": email, "msg": "密码不一致"})
            # 如果密码一致
            # 找到激活码对应的邮箱
            all_record = EmailVerifyCode.objects.filter(code=active_code)
            for record in all_record:
                email = record.email

            user = UserProfile.objects.get(email=email)
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return render(request, "login.html", {"msg": "密码修改成功，请登录"})
        # 验证失败说明密码位数不够。
        else:
            email = request.POST.get("email", "")
            return render(
                request, "password_reset.html", {
                    "email": email, "modifypwd_form": modifypwd_form})

class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')[:5]

        courses = Course.objects.filter(is_banner=False)[:6]

        banner_courses = Course.objects.filter(is_banner=True)[:3]

        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'all_banner': all_banner,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })
