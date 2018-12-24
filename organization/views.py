#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from organization.forms import UserAskForm
from django.shortcuts import render
from django.views.generic import View
from organization.models import CourseOrg, CityDict,Teacher
from operation.models import UserFavorite
from courses.models import Course
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()

        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_citys = CityDict.objects.all()

        #机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter( Q(name__icontains=search_keywords)|
                                        Q(desc__icontains=search_keywords) )

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=(int(city_id)))

        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        
        org_nums = all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, "org_list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })

class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"Wrong information, please check"}', content_type='application/json')

class OrgHomeView(View):
    
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]

        return render(request, 'org_detail_homepage.html', {
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
    })


class OrgCourseView(View):

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()

        return render(request, 'org_detail_course.html', {
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgDescView(View):
    
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org_detail_desc.html', {
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgTeacherView(View):
    
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()

        return render(request, 'org_detail_teachers.html', {
            'course_org':course_org,
            'all_teachers':all_teachers,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class AddFavView(View):
    
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

class TeacherListView(View):
    """
    课程讲师列表
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()

        #讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter( Q(name__icontains=search_keywords) )
        
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:2]

        #对讲师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)

        return render(request, 'teachers_list.html', {
            'all_teachers': teachers,
            'sort': sort,
            'sorted_teacher': sorted_teacher,
        })

class TeacherDetailView(View):

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()

        #讲师课程
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        #讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:2]
        return render(request, 'teacher_detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,

        })
