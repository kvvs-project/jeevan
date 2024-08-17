from django.urls import path
from . import views

urlpatterns = [
    path('find', views.find_donors, name="find"),
    path('organ-match', views.guest_find_organ_donor, name="guest_find_organ_donor"),
    path('get-organ-match', views.guest_get_organ_hospital_list, name="guest_get_organ_hospital_list"),
    path('blood-match', views.guest_find_blood_donor, name="guest_find_blood_donor"),
    path('get-blood-match', views.guest_get_blood_donor_list, name="guest_get_blood_donor_list"),
]