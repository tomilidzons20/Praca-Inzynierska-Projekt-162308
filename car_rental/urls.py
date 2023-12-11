from django.urls import path


from .views import HomeView
from .views import NewsDetailView
from .views import NewsListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
]
