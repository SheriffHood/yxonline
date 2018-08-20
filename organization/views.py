#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from organization.models import CourseOrg, CityDict

from pure_pagination import Paginator, 

# Create your views here.
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()

        return render(request, "org_list.html", {
            "all_orgs":all_orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
        })
