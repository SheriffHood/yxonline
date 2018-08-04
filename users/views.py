#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg':'Already exists'})
            pass_word = request.POST.get('password', "")

            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg':'Wrong username or password!'})
        else:
            return render(request, 'login.html', {'login_form':login_form})
