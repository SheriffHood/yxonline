#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render

def login(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return render(request, 'login.html', {})
