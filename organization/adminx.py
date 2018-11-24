#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import xadmin
from organization.models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'category', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'category', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'category', 'click_nums', 'fav_nums', 'city', 'address', 'add_time']

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
