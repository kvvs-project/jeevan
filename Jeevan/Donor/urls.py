from django.urls import path
from . import views

urlpatterns = [
    path('onboarding', views.donor_pre_reg, name="donor_pre_reg"),
    path('select-hospital', views.donor_find_hospital, name="donor_find_hospital"),
    path('signup', views.donor_reg, name="donor_reg"),
    path('sign-up', views.validate_donor_reg, name="validate_donor_reg"),
    path('new-organ-donation', views.donor_new_organ_donation, name="donor_new_organ_donation"),
    path('validate-new-organ-donation', views.validate_donor_new_organ_donation, name="validate_donor_new_organ_donation"),
    path('view-organ-donation-status', views.donor_organ_donation_status, name="donor_organ_donation_status"),
    path('cancel-organ-donation', views.donor_cancel_organ_donation, name="donor_cancel_organ_donation"),
    path('validate-cancel-organ-donation', views.validate_donor_cancel_organ_donation, name="validate_donor_cancel_organ_donation"),
]