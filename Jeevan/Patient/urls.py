from django.urls import path
from . import views

urlpatterns = [
    path('select-hospital', views.patient_pre_reg, name="patient_pre_reg"),
    path('signup', views.patient_reg, name="patient_reg"),
    path('sign-up', views.validate_patient_reg, name="validate_patient_reg"),
    path('organ-match', views.patient_make_new_organ_request, name="patient_make_new_organ_request"),
    path('organ-match-list', views.patient_get_organ_hospital_list, name="patient_get_organ_hospital_list"),
    path('organ-match-details', views.patient_make_organ_donation_request, name="patient_make_organ_donation_request"),
    path('get-organ-match', views.patient_validate_organ_donation_request, name="patient_validate_organ_donation_request"),
    path('organ-match-status', views.patient_organ_request_status, name="patient_organ_request_status"),
    path('get-organ-match-details', views.patient_organ_request_details, name="patient_organ_request_details"),
    path('cancel-organ-match', views.patient_cancel_organ_request, name="patient_cancel_organ_request"),
    path('get-cancel-organ-match', views.validate_patient_cancel_organ_request, name="validate_patient_cancel_organ_request")
]