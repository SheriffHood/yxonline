#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', "")
        pass_word = request.POST.get('password', "")

        user = authenticate(username=user_name, password=pass_word)

        if user is not None:
            login(request, user)
    elif request.method == 'GET':
        return render(request, 'login.html', {})
