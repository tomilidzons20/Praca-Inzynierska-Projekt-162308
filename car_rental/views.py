from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'car_rental/home.html'


class DashboardHomeView(TemplateView):
    template_name = 'car_rental/dashboard/home.html'
