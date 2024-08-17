from django.urls import path
from django.urls import include

from Main import views

urlpatterns = [
    path('', views.home_page),
    path('pwa', views.home_page),
    path('login', views.user_login, name="login"),
    path('get-login', views.validate_login, name="get_login"),
    path('signup', views.signup_page, name="signup"),
    path('admin/', include('Admin.urls')),
    path('guest/', include('Guest.urls')),
    path('donor/', include('Donor.urls')),
    path('patient/', include('Patient.urls')),
    path('hospital/', include('Hospital.urls')),
    path('favicon.ico', views.serve_favicon),
]
