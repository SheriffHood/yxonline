#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import xadmin
from organization.models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_dispay = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

class CourseOrgAdmin(object):
    list_dispay = ['name', 'desc', 'catetory', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'catetory', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'catetory', 'click_nums', 'fav_nums', 'city_name', 'address', 'add_time']

class TeacherAdmin(object):
    list_dispay = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)