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
    admin_validate_add_new_organ, donor_pre_reg, donor_reg, validate_donor_reg, patient_pre_reg, patient_reg, \
    validate_patient_reg, patient_approval, show_patient_details, validate_patient_approval, download_patient_report, \
    guest_find_organ_donor, guest_get_organ_hospital_list, patient_make_new_organ_request, \
    patient_get_organ_hospital_list, patient_make_organ_donation_request, patient_validate_organ_donation_request, \
    hospital_organ_request_approval, hospital_show_organ_approval_details, hospital_validate_organ_request_approval, \
    patient_organ_request_status, patient_organ_request_details, hospital_cancel_patient_organ_request, \
    validate_hospital_cancel_patient_organ_request, validate_patient_cancel_organ_request, patient_cancel_organ_request, \
    hospital_organ_transplantation, hospital_organ_transplantation_details, hospital_organ_transplantation_entry, \
    validate_hospital_organ_transplantation_entry, guest_find_blood_donor, guest_get_blood_donor_list, \
    hospital_find_blood_donor, hospital_get_blood_donor_list, hospital_get_blood_donor_details, \
    hospital_validate_blood_donation, serve_favicon

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', serve_favicon),
    path('pwa', home_page),
    path('', home_page),
    path('login', user_login),
    path('get_login', validate_login),
    path('change_admin_pass', admin_change_pass),
    path('check_admin_pass', admin_validate_change_pass),
    path('hospital_reg', hospital_reg),
    path('get_hreg', validate_hospital_reg),
    path('hospital_approval', hospital_approval),
    path('show_hospital_details', show_hospital_details),
    path('download_hospital_proof', download_hospital_proof),
    path('validate_hospital_approval', validate_hospital_approval),
    path('hospital_organ_request_approval', hospital_organ_request_approval),
    path('hospital_show_organ_approval_details', hospital_show_organ_approval_details),
    path('hospital_find_blood_donor', hospital_find_blood_donor),
    path('hospital_get_blood_donor_list', hospital_get_blood_donor_list),
    path('hospital_get_blood_donor_details', hospital_get_blood_donor_details),
    path('hospital_validate_blood_donation', hospital_validate_blood_donation),
    path('hospital_organ_transplantation', hospital_organ_transplantation),
    path('hospital_cancel_patient_organ_request', hospital_cancel_patient_organ_request),
    path('hospital_organ_transplantation_details', hospital_organ_transplantation_details),
    path('hospital_organ_transplantation_entry', hospital_organ_transplantation_entry),
    path('validate_hospital_organ_transplantation_entry', validate_hospital_organ_transplantation_entry),
    path('hospital_validate_organ_request_approval', hospital_validate_organ_request_approval),
    path('validate_hospital_cancel_patient_organ_request', validate_hospital_cancel_patient_organ_request),
    path('donor_pre_reg', donor_pre_reg),
    path('donor_reg', donor_reg),
    path('validate_donor_reg', validate_donor_reg),
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
    path('patient_pre_reg', patient_pre_reg),
    path('patient_reg', patient_reg),
    path('validate_patient_reg', validate_patient_reg),
    path('patient_approval', patient_approval),
    path('show_patient_details', show_patient_details),
    path('validate_patient_approval', validate_patient_approval),
    path('patient_make_new_organ_request', patient_make_new_organ_request),
    path('patient_get_organ_hospital_list', patient_get_organ_hospital_list),
    path('patient_make_organ_donation_request', patient_make_organ_donation_request),
    path('patient_validate_organ_donation_request', patient_validate_organ_donation_request),
    path('download_patient_report', download_patient_report),
    path('guest_find_organ_donor', guest_find_organ_donor),
    path('guest_get_hospital_list', guest_get_organ_hospital_list),
    path('guest_find_blood_donor', guest_find_blood_donor),
    path('guest_get_blood_donor_list', guest_get_blood_donor_list),
    path('patient_organ_request_status', patient_organ_request_status),
    path('patient_organ_request_details', patient_organ_request_details),
    path('patient_cancel_organ_request', patient_cancel_organ_request),
    path('validate_patient_cancel_organ_request', validate_patient_cancel_organ_request)
]

