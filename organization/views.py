#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from organization.models import CourseOrg, CityDict
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, "org_list.html", {
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
        })
