#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')

        user = authenticate(username=user_name, password=pass_word)

        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {})
