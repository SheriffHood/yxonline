#!/usr/bin/env python3
#-*- coding:utf8 -*-

from datetime import datetime

from django.db import models

from organization.models import CourseOrg

class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', u'初级'),
        ('zj', u'中级'),
        ('gj', u'高级')
    )

    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(
        upload_to='courses/%Y/%M',
        verbose_name=u'封面图',
        max_length=100
    )
    click_nums = models.IntegerField(default=0, verbose_name=u'点击次数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'课程'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'章节'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '<{0}>课程章节 >> {1} '.format(self.course, self.name)

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'视频'
        verbose_name_plural=verbose_name

class CourseResource(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程') 
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(
        upload_to='course/resource/%Y/%M',
        verbose_name=u'资源文件',
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'课程资源'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '<{0}>课程资源 >> {1} '.format(self.course, self.name)
