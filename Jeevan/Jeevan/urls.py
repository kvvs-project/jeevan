from django.urls import path
from django.urls import include

from Main import views

urlpatterns = [
    path('', views.home_page),
    path('pwa', views.home_page),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('thanks', views.thanks),
    path('get-login', views.validate_login, name="get_login"),
    path('signup', views.signup_page, name="signup"),
    path('privacy', views.privacy_policy, name="privacy_policy"),
    path('tos', views.terms_of_service, name="terms_of_service"),
    path('about', views.about_us, name="about_us"),
    path('change-password', views.change_pass, name="change_pass"),
    path('check-password', views.validate_change_pass, name="check_pass"),
    path('admin/', include('Admin.urls')),
    path('guest/', include('Guest.urls')),
    path('donor/', include('Donor.urls')),
    path('patient/', include('Patient.urls')),
    path('hospital/', include('Hospital.urls')),
    path('favicon.ico', views.serve_favicon),
    path('error', views.error_msg, name="error")
]
