from django.urls import path, include
from . import views


urlpatterns= [
    path('authenticate/', include('djoser.urls')),
    path("Create/", include('djoser.urls.jwt')),
    path("Login/", views.login_view, name= 'login'),
    path("Logout/", views.logout_view, name= 'logout')
]