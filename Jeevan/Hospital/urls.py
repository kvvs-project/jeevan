from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.hospital_reg, name="hospital_reg"),
    path('sign-up', views.validate_hospital_reg, name="get_hreg"),
    path('donor-approval', views.donor_approval, name="donor_approval"),
    path('show-donor-details', views.show_donor_details, name="show_donor_details"),
    path('validate-donor-approval', views.validate_donor_approval, name="validate_donor_approval"),
    path('download-donor-report', views.download_donor_report, name="download_donor_report"),
    path('patient-approval', views.patient_approval, name="patient_approval"),
    path('show-patient-details', views.show_patient_details, name="show_patient_details"),
    path('validate-patient-approval', views.validate_patient_approval, name="validate_patient_approval"),
    path('download-patient-report', views.download_patient_report, name="download_patient_report"),
    path('find-blood-donor', views.hospital_find_blood_donor, name="hospital_find_blood_donor"),
    path('get-blood-donor-list', views.hospital_get_blood_donor_list, name="hospital_get_blood_donor_list"),
    path('get-blood-donor-details', views.hospital_get_blood_donor_details, name="hospital_get_blood_donor_details"),
    path('validate-blood-donation', views.hospital_validate_blood_donation, name="hospital_validate_blood_donation"),
    path('organ-transplantation', views.hospital_organ_transplantation, name="hospital_organ_transplantation"),
    path('view-organ-transplantation-details', views.hospital_organ_transplantation_details, name="hospital_organ_transplantation_details"),
    path('organ-transplantation-entry', views.hospital_organ_transplantation_entry, name="hospital_organ_transplantation_entry"),
    path('validate-organ-transplantation-entry', views.validate_hospital_organ_transplantation_entry, name="validate_hospital_organ_transplantation_entry"),
    path('organ-request-approval', views.hospital_organ_request_approval, name="hospital_organ_request_approval"),
    path('view-organ-approval-details', views.hospital_show_organ_approval_details, name="hospital_show_organ_approval_details"),
    path('validate-organ-request-approval', views.hospital_validate_organ_request_approval, name="hospital_validate_organ_request_approval"),
    path('cancel-patient-organ-request', views.hospital_cancel_patient_organ_request, name="hospital_cancel_patient_organ_request"),
    path('validate-cancel-patient-organ-request', views.validate_hospital_cancel_patient_organ_request, name="validate_hospital_cancel_patient_organ_request"),
]
