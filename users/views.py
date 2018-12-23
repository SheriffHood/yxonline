#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import json

from users.models import UserProfile, EmailVerifyCode
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.http import HttpResponse

from users.forms import LoginForm, RegisterForm, ModifyPwdForm, ForgetPwdForm, ActiveForm, UploadImageForm
from users.forms import UserInfoForm
from utils.send_email import send_register_mail
from users.models import Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course

from utils.mixin_utils import LoginRequiredMixin
from utils.send_email import send_register_mail


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

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

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "Welcome to Hood"
            user_message.save()
            
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

class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter_info.html', {
            
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UpdatePwdView(LoginRequiredMixin ,View):
    """
    个人中心修改用户密码
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            # 如果密码一致
            user = request.user
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        # 验证失败说明密码位数不够。
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin ,View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"fail", "msg":"邮箱已经存在"}', content_type='application/json')

        send_register_mail(email, 'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyCode.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": success}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')

class MyCourseView(LoginRequiredMixin, View):
    """
    用户课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter_mycourse.html', {
            'user_courses':user_courses,
        })

class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.filter(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter_fav_org.html', {
            'org_list':org_list,
        })

class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的教师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.filter(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter_fav_teacher.html',{
            'teacher_list':teacher_list,
        })

class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.filter(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter_fav_course.html',{
            'course_list':course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter_message.html', {
            'messages':messages,
        })
