from django.urls import path
from . import views

urlpatterns = [
    path('change-password', views.admin_change_pass, name="change_admin_pass"),
    path('check_password', views.admin_validate_change_pass, name="check_admin_pass"),
    path('view-organ-list', views.admin_organ_list, name="admin_organ_list"),
    path('add-new-organ', views.admin_add_new_organ, name="admin_add_new_organ"),
    path('validate-add-new_organ', views.admin_validate_add_new_organ, name="admin_validate_add_new_organ"),
    path('hospital-approval', views.hospital_approval, name="hospital_approval"),
    path('view-hospital-details', views.show_hospital_details, name="show_hospital_details"),
    path('download-hospital-proof', views.download_hospital_proof, name="download_hospital_proof"),
    path('validate-hospital-approval', views.validate_hospital_approval, name="validate_hospital_approval")
]
