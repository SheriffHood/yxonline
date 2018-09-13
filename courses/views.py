#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from courses.models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class CourseListView(View):
    def get(self, request):

        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course_list.html', {
            'all_courses':courses,
            'hot_courses':hot_courses,
            'sort':sort,    
        })
