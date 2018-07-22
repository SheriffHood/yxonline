#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from users.models import UserProfile

from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
