from django.urls import include
from django.urls import path

from .views import CustomPasswordChangeView
from .views import ProfileView
from .views import address_update_view
from .views import cancel_rental_view

urlpatterns = [
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_password_change'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', ProfileView.as_view(), name='view_profile'),
    path('accounts/profile/update-address', address_update_view, name='update_address'),
    path('accounts/profile/cancel-rental', cancel_rental_view, name='cancel_rental'),
]
