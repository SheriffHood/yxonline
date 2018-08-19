#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class OrgView(View):
    def get(self, request):
        return render(request, "org_list.html", {})