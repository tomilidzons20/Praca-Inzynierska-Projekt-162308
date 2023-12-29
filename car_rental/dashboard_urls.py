from django.urls import path

from .dashboard_views import DashboardCarListView
from .dashboard_views import DashboardCarUpdateView
from .dashboard_views import DashboardContactListView
from .dashboard_views import DashboardContactUpdateView
from .dashboard_views import DashboardHomeView
from .dashboard_views import DashboardMaintenanceListView
from .dashboard_views import DashboardMaintenanceUpdateView
from .dashboard_views import DashboardNewsListView
from .dashboard_views import DashboardNewsUpdateView
from .dashboard_views import DashboardRentalExtraListView
from .dashboard_views import DashboardRentalExtraUpdateView
from .dashboard_views import DashboardRentalListView
from .dashboard_views import DashboardRentalProtectionListView
from .dashboard_views import DashboardRentalProtectionUpdateView
from .dashboard_views import DashboardRentalUpdateView
from .dashboard_views import car_create_view
from .dashboard_views import contact_create_view
from .dashboard_views import maintenance_create_view
from .dashboard_views import news_create_view
from .dashboard_views import rental_create_view
from .dashboard_views import rental_extra_create_view
from .dashboard_views import rental_protection_create_view

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard_home'),

    path('cars/', DashboardCarListView.as_view(), name='dashboard_car_list'),
    path('cars/create/', car_create_view, name='dashboard_car_create'),
    path('cars/update/<int:pk>/', DashboardCarUpdateView.as_view(), name='dashboard_car_update'),

    path('maintenance/', DashboardMaintenanceListView.as_view(), name='dashboard_maintenance_list'),
    path('maintenance/create/', maintenance_create_view, name='dashboard_maintenance_create'),
    path('maintenance/update/<int:pk>/', DashboardMaintenanceUpdateView.as_view(), name='dashboard_maintenance_update'),

    path('rentals/', DashboardRentalListView.as_view(), name='dashboard_rental_list'),
    path('rentals/create/', rental_create_view, name='dashboard_rental_create'),
    path('rentals/update/<int:pk>/', DashboardRentalUpdateView.as_view(), name='dashboard_rental_create'),

    path('contacts/', DashboardContactListView.as_view(), name='dashboard_contact_list'),
    path('contacts/create/', contact_create_view, name='dashboard_contact_create'),
    path('contacts/update/<int:pk>/', DashboardContactUpdateView.as_view(), name='dashboard_contact_update'),

    path('protections/', DashboardRentalProtectionListView.as_view(), name='dashboard_protection_list'),
    path('protections/create/', rental_protection_create_view, name='dashboard_protection_create'),
    path(
        'protections/update/<int:pk>/',
        DashboardRentalProtectionUpdateView.as_view(),
        name='dashboard_protection_update'
    ),

    path('extras/', DashboardRentalExtraListView.as_view(), name='dashboard_extra_list'),
    path('extras/create/', rental_extra_create_view, name='dashboard_extra_create'),
    path('extras/update/<int:pk>/', DashboardRentalExtraUpdateView.as_view(), name='dashboard_extra_update'),

    path('news/', DashboardNewsListView.as_view(), name='dashboard_news_list'),
    path('news/create/', news_create_view, name='dashboard_news_create'),
    path('news/update/<int:pk>/', DashboardNewsUpdateView.as_view(), name='dashboard_news_update'),
]
