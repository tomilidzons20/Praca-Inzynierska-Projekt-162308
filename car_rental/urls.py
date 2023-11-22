from django.urls import path

from .views import HomeView
from .views import DashboardHomeView
from .views import DashboardCarListView
from .views import DashboardCarCreateView
from .views import DashboardCarUpdateView
from .views import DashboardMaintenanceListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardHomeView.as_view(), name='dashboard_home'),
    path('dashboard/cars', DashboardCarListView.as_view(), name='dashboard_car_list'),
    path('dashboard/cars/create', DashboardCarCreateView.as_view(), name='dashboard_car_create'),
    path('dashboard/cars/update/<int:pk>/', DashboardCarUpdateView.as_view(), name='dashboard_car_update'),
    path('dashboard/maintenance/', DashboardMaintenanceListView.as_view(), name='dashboard_maintenance_list'),
]
