"""
URL configuration for srms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from App1 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('sreg/',views.sreg,name='reg'),
    path('',views.home,name='home'),
    path('role/',views.role,name='role'),
    path('shome/<int:id>',views.shome,name='shome'),
    path('schedule/<int:id>',views.schedule,name='schedule'),
    path('e-reg/<int:id>',views.e_reg,name='exam-reg'),
    path('im/<int:id>',views.im,name='int-marks'),
    path('eim/<int:id>',views.eim,name='eim'),
    path('sr/<int:id>',views.sr,name='sem-res'),
    path('tlogin/',views.tlogin,name='tlogin'),
    path('thome/<int:id>',views.thome,name='thome'),
    path('alogin/',views.alogin,name='alogin'),
     path('entry/<int:id>',views.marks_entry,name='marks_entry'),
    path('abase/',views.abase,name='abase'),
    path('treg/',views.treg,name='treg'),
    path('cp/<int:id>',views.cp,name='cp'),
    path('reports/<int:id>',views.reports,name='reports'),
    path('pr/',views.pr,name='pr'),
    path('npr/',views.npr,name='npr'),
    path('smsg/',views.smsg,name='smsg'),
    path('notfound/',views.notfound,name='nf'),
    path('cancel-msg/',views.cmsg,name='cmsg')
    # path('tme/<int:id>',views.tme,name='tme'),
]
