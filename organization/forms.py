#!usr/bin/env python3 
#-*- coding:utf-8 -*-

from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']
