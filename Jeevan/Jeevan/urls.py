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
    hospital_reg, validate_hospital_reg, hospital_approval, show_hospital_details, validate_hospital_approval, \
    download_hospital_proof, donor_approval, show_donor_details, validate_donor_approval, download_donor_report, \
    donor_new_organ_Donation, validate_donor_new_organ_donation, donor_organ_donation_status, \
    donor_cancel_organ_donation, validate_donor_cancel_organ_donation, admin_organ_list, admin_add_new_organ, \
    admin_validate_add_new_organ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('login', user_login),
    path('get_login', validate_login),
    path('change_admin_pass', admin_change_pass),
    path('check_admin_pass', admin_validate_change_pass),
    path('hospital_reg', hospital_reg),
    path('hospital_approval', hospital_approval),
    path('show_hospital_details', show_hospital_details),
    path('validate_hospital_approval', validate_hospital_approval),
    path('download_hospital_proof', download_hospital_proof),
    path('get_hreg', validate_hospital_reg),
    path('donor_approval', donor_approval),
    path('show_donor_details', show_donor_details),
    path('validate_donor_approval', validate_donor_approval),
    path('download_donor_report', download_donor_report),
    path('donor_new_organ_Donation', donor_new_organ_Donation),
    path('validate_donor_new_organ_donation', validate_donor_new_organ_donation),
    path('donor_organ_donation_status', donor_organ_donation_status),
    path('donor_cancel_organ_donation', donor_cancel_organ_donation),
    path('validate_donor_cancel_organ_donation', validate_donor_cancel_organ_donation),
    path('admin_organ_list', admin_organ_list),
    path('admin_add_new_organ', admin_add_new_organ),
    path('admin_validate_add_new_organ', admin_validate_add_new_organ),
]

