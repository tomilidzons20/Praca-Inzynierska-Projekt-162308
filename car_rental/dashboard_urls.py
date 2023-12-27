from django.urls import path

from .dashboard_views import DashboardCarListView
from .dashboard_views import DashboardCarUpdateView
from .dashboard_views import DashboardHomeView
from .dashboard_views import DashboardMaintenanceListView
from .dashboard_views import DashboardRentalListView
from .dashboard_views import rental_create_view
from .dashboard_views import maintenance_create_view
from .dashboard_views import car_create_view

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('cars/', DashboardCarListView.as_view(), name='dashboard_car_list'),
    path('cars/update/<int:pk>/', DashboardCarUpdateView.as_view(), name='dashboard_car_update'),
    path('maintenance/', DashboardMaintenanceListView.as_view(), name='dashboard_maintenance_list'),
    path('rentals/', DashboardRentalListView.as_view(), name='dashboard_rental_list'),
    path('rentals/create/', rental_create_view, name='dashboard_rental_create'),
    path('maintenance/create/', maintenance_create_view, name='dashboard_maintenance_create'),
    path('cars/create/', car_create_view, name='dashboard_car_create'),
]
