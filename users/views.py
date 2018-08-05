#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.models import UserProfile
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.views.generic import TemplateView

def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        user = authenticate(username= user_name, password= pass_word)

        if user is not None:
            login(request, user)
            return render(request, "index.html")
      
        else:
            return render(request, "login.html", {})

