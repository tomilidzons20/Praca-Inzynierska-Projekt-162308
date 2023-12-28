from django.urls import path

from .views import CarRentalForDaysView
from .views import ContactCreateView
from .views import HomeView
from .views import NewsDetailView
from .views import NewsListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('days-rental/', CarRentalForDaysView.as_view(), name='days_rental'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
]
