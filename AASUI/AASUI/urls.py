"""AASUI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from home import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^digitalEyeAdmin/', admin.site.urls),
    url(r'^$',views.rhome,name="rhome"),
    url(r'^home',views.index,name="home"),
    url(r'^login',views.login,name="login"),
    url(r'^logout',views.logout,name="logout"),
    url(r'^help',views.help,name="help"),
    url(r'^admin/domore',views.domore,name='domore'),
    url(r'^mupload',views.mupload,name='mupload'),
    url(r'^history/$',views.history,name="history"),
    url(r'^webcamcapture/$',views.webcamcapture,name="webcamcapture"),
    url(r'^webcamimage/$',views.webcamimage,name="webcamimage"),
    url(r'^startcapturing/$',views.startcapturing,name="startcapturing"),
    url(r'^done/$',views.done,name="done"),
    url(r'^profile/$',views.profile,name="profile"),
    url(r'^ipwebcamcapture/$',views.ipwebcamcapture,name="ipwebcamcapture"),
    url(r'^ipcamimage/$',views.ipcamimage,name="ipcamimage"),
    #paras
    url(r'^admin/dataenter/$',views.dataenter,name="dataenter"),
    url(r'^startentering/$',views.startentering,name="startentering"),
    url(r'^admin/dataenter/dataenterusingwebcam/$',views.dataenterusingwebcam,name="dataenterusingwebcam"),
    url(r'^admin/dataenter/dataenterusingipwebcam/$',views.dataenterusingipwebcam,name="dataenterusingipwebcam"),
    url(r'^webcamdataenterimage/$',views.webcamdataenterimage,name="webcamdataenterimage"),
    url(r'^ipcamdataenterimage/$',views.ipcamdataenterimage,name="ipcamdataenterimage"),
    #auth
    url(r'^admin/$',views.admin,name="admin"),
    url(r'^admin/login/$', auth_views.login),
    url(r'^admin/logout/$',view=logout,kwargs={'next_page': '/'},name='adminlogout'),
    url(r'^admin/help$',views.adminhelp,name="adminhelp"),

    #ashok download
    url(r'^download/$',views.download,name='downlaod'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
