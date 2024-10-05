from django.urls import path
from . import views

urlpatterns = [
    path('view-organ-list', views.admin_organ_list, name="admin_organ_list"),
    path('add-new-organ', views.admin_add_new_organ, name="admin_add_new_organ"),
    path('validate-add-new_organ', views.admin_validate_add_new_organ, name="admin_validate_add_new_organ"),
    path('hospital-approval', views.hospital_approval, name="hospital_approval"),
    path('show-hospital-details', views.show_hospital_details, name="show_hospital_details"),
    path('download-hospital-proof', views.download_hospital_proof, name="download_hospital_proof"),
    path('validate-hospital-approval', views.validate_hospital_approval, name="validate_hospital_approval"),
    path('users', views.view_users, name="admin_view_users" ),
    path('hospital-list', views.hospital_list, name="admin_hospital_list" ),
    path('select-hospital-list', views.validate_hospital_list, name="admin_validate_hospital_list" ),
    path('view-hospital-details', views.view_hospital_details, name="admin_hospital_details" ),
    path('donor-list', views.donor_list, name="admin_donor_list" ),
    path('select-donor-list', views.validate_donor_list, name="admin_validate_donor_list" ),
    path('view-donor-details', views.view_donor_details, name="admin_donor_details" ),
    path('patient-list', views.patient_list, name="admin_patient_list" ),
    path('select-patient-list', views.validate_patient_list, name="admin_validate_patient_list" ),
    path('view-patient-details', views.view_patient_details, name="admin_patient_details" ),
]
