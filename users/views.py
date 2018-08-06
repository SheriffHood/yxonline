#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.models import UserProfile
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.db.models import Q

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
