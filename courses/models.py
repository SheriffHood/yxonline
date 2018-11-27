#!/usr/bin/env python3
#-*- coding:utf8 -*-

from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher

class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', u'初级'),
        ('zj', u'中级'),
        ('gj', u'高级')
    )

    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"课程机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u"讲师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    notes = models.CharField(max_length=300, default=u"study hard", verbose_name=u"课程须知")
    known = models.CharField(max_length=300, default=u"study hard", verbose_name=u"老师告诉你")
    image = models.ImageField(
        default="",
        upload_to='courses/%Y/%M',
        verbose_name=u'封面图',
        max_length=100
    )
    click_nums = models.IntegerField(default=0, verbose_name=u'点击次数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name=u'课程类别')
    tag = models.CharField(default="", max_length=10, verbose_name=u'课程标签')

    class Meta:
        verbose_name=u'课程'
        verbose_name_plural=verbose_name

    def get_section_nums(self):
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

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
        return '<{0}>课程的章节 >> {1} '.format(self.course, self.name)

    def get_lesson_video(self):
        return self.video_set.all()

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'视频'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '<{0}>章节的视频 >> {1} '.format(self.lesson, self.name)

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
        return '<{0}>课程的资源 >> {1} '.format(self.course, self.name)
