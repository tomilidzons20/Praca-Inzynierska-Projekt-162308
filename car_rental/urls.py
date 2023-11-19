from django.urls import path

from .views import HomeView
from .views import DashboardHomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardHomeView.as_view(), name='dashboard_home'),
]
