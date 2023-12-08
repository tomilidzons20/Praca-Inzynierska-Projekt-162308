from django.urls import path

from .api_views import MaintenanceCreateAPIView
from .dashboard_views import DashboardCarCreateView
from .dashboard_views import DashboardCarListView
from .dashboard_views import DashboardCarUpdateView
from .dashboard_views import DashboardHomeView
from .dashboard_views import DashboardMaintenanceListView
from .dashboard_views import DashboardRentalListView
from .dashboard_views import DashboardRentalCreateView

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('cars/', DashboardCarListView.as_view(), name='dashboard_car_list'),
    path('cars/create/', DashboardCarCreateView.as_view(), name='dashboard_car_create'),
    path('cars/update/<int:pk>/', DashboardCarUpdateView.as_view(), name='dashboard_car_update'),
    path('maintenance/', DashboardMaintenanceListView.as_view(), name='dashboard_maintenance_list'),
    path('rentals/', DashboardRentalListView.as_view(), name='dashboard_rental_list'),
    path('rentals/create/', DashboardRentalCreateView.as_view(), name='dashboard_rental_create'),
    path('api/maintenance/create/', MaintenanceCreateAPIView.as_view(), name='api_maintenance_create'),
]
