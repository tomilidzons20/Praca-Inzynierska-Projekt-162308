from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView

from .models import Car
from .forms import CarForm


class HomeView(TemplateView):
    template_name = 'car_rental/home.html'


class DashboardHomeView(TemplateView):
    template_name = 'car_rental/dashboard/home.html'


class DashboardCarListView(ListView):
    template_name = 'car_rental/dashboard/car_list.html'
    model = Car
    paginate_by = 10


class DashboardCarCreateView(CreateView):
    template_name = 'car_rental/dashboard/car_create.html'
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy('dashboard_car_list')
