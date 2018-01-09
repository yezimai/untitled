"""untitled URL Configuration

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
from django.conf.urls import url
from account import views

urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view(),name="register" ),
    url(r'^send_mail_success/$',views.send_mail_success,name="send_mail_success" ),
    url(r'^check_username/$',views.check_username,name="check_username" ),
    url(r'^login/',views.LoginView,name="login" ),
    url(r'^modify/', views.ModifyView.as_view(), name="forget_password"),
    url(r'^active/(?P<active_code>.*)/$',views.ActiveView.as_view(), name='active'),
    url(r'^modify_password/(?P<reset_code>.*)/$',views.ModifyPasswordView.as_view(), name='modify_password'),
    url(r'^logout/',views.logout_view,name="logout" ),
    url(r'^user_center_info/', views.user_center_info, name="user_center_info"),
    url(r'^user_center_site/', views.user_center_site, name="user_center_site"),
    url(r'^user_center_set_default_site/', views.user_center_set_default_site, name="user_center_set_default_site"),
    url(r'^user_center_del_default_site/', views.user_center_del_default_site, name="user_center_del_default_site"),

]
