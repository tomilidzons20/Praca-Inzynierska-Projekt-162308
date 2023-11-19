from django.urls import path
from django.urls import include

from .views import ProfileView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', ProfileView.as_view(), name="view_profile"),
]
