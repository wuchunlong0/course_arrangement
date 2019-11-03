"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView  
from account import views
urlpatterns = [
    url(r'^test/$', views.test, name="test"),
    
    url(r'^choice/(?P<page>\d*)?$', views.choice, name="choice"),
    
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),

    url(r'^classromm/list/$', views.classromm_list, name="classromm_list"),
    url(r'^schedule/list/(?P<page>\d*)?$', views.schedule_list, name="schedule_list"),
    url(r'^romm/list/(?P<page>\d*)?$', views.romm_list, name="romm_list"),  
    url(r'^schedule/import/$', views.schedule_import, name="schedule_import"),
    url(r'^classromm/import/$', views.classromm_import, name="classromm_import"),

    url(r'^building/list/$', views.building_list, name="building_list"),
    url(r'^room/list/$', views.room_list, name="room_list"),
    url(r'^kcmc/details/$', views.kcmc_details, name="kcmc_details"),
    
    url(r'^self/study/list/$', views.self_study_list, name="self_study_list"),
    url(r'^self/building/list/$', views.self_building_list, name="self_building_list"), 
    
    url(r'^schedule/filter/$', views.schedule_filter, name="schedule_filter"),
    url(r'^course/list/$', views.course_list, name="course_list"),      
    
    url(r'^classname/list/(?P<page>\d*)?$', views.classname_list, name="classname_list"), 
    url(r'^teacher/list/(?P<page>\d*)?$', views.teacher_list, name="teacher_list"),
    
    url(r'^all/list/$', views.all_list, name="all_list"),
    
    url(r'^', views.query_list, name="query_list"),    
]
