from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django_filters.views import FilterView

from .models import Car
from .models import CarMaintenance
from .models import CarRental


class HomeView(TemplateView):
    template_name = 'car_rental/home.html'



