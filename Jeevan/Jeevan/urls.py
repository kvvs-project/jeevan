"""
URL configuration for Jeevan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from JeevanApp.views import home_page, validate_login, user_login, admin_validate_change_pass, admin_change_pass, \
    hospital_reg, validate_hospital_reg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('login', user_login),
    path('get_login', validate_login),
    path('change_admin_pass', admin_change_pass),
    path('check_admin_pass', admin_validate_change_pass),
    path('hospital_reg', hospital_reg),
    path('get_hreg', validate_hospital_reg)
]

