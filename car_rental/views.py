from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .models import News


class HomeView(TemplateView):
    template_name = 'car_rental/main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = News.objects.all().order_by('-add_date')[:3]
        return context


class NewsListView(ListView):
    model = News
    template_name = 'car_rental/main/news.html'

    def get_queryset(self):
        return News.objects.all().order_by('-add_date')


class NewsDetailView(DetailView):
    model = News
    template_name = 'car_rental/main/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_news'] = News.objects.filter(add_date__lt=self.object.add_date).order_by('-add_date').first()
        context['next_news'] = News.objects.filter(add_date__gt=self.object.add_date).order_by('add_date').first()
        return context

