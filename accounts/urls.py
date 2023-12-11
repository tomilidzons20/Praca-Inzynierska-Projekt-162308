from django.urls import include
from django.urls import path

from .views import ProfileView
from .views import address_update_view

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', ProfileView.as_view(), name="view_profile"),
    path('accounts/profile/update-address', address_update_view, name="update_address"),
]
