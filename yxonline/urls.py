"""yxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
import xadmin
from users import views
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from yxonline.settings import MEDIA_ROOT
from organization.views import OrgView
from django.views.static import serve

xadmin.autodiscover()

from xadmin.plugins import xversion
from django.views.generic import TemplateView
from users.views import IndexView, LogoutView, RegisterView, ModifyPwdView, ForgetPwdView

xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    #path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('', IndexView.as_view(), name = 'index'),

    path('login/', LoginView.as_view(), name="login"),

    #退出登录
    path('logout/', LogoutView.as_view(), name='logout'),

    path("register/", RegisterView.as_view(), name = "register" ),

    path("captcha/", include('captcha.urls')),

    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name= "user_active"),

    path('forget/', ForgetPwdView.as_view(), name= "forget_pwd"),

    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),

    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),

    path("org/", include('organization.urls', namespace='org')),

    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),

    #re_path('static/(?P<path>.*)', serve, {"document_root": STATICFILES_DIRS }),

    path('course/', include('courses.urls', namespace='course')),

    path('users/', include('users.urls', namespace='users')),

]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
