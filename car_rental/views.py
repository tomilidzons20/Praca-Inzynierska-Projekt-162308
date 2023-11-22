from django.shortcuts import render
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView

from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .forms import CarForm


class HomeView(TemplateView):
    template_name = 'car_rental/home.html'


class DashboardHomeView(TemplateView):
    template_name = 'car_rental/dashboard/home.html'


class DashboardCarListView(ListView):
    template_name = 'car_rental/dashboard/car_list.html'
    model = Car
    paginate_by = 10
    ordering = 'brand'


class DashboardCarCreateView(CreateView):
    template_name = 'car_rental/dashboard/car_create.html'
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy('dashboard_car_list')


class DashboardCarUpdateView(UpdateView):
    template_name = 'car_rental/dashboard/car_update.html'
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy('dashboard_car_update', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maintenance_list = CarMaintenance.objects.filter(car=self.object.id)
        context['maintenance_list'] = maintenance_list
        total_maintenance_cost = maintenance_list.aggregate(
            Sum('cost_of_repair')
        )['cost_of_repair__sum']
        context['total_maintenance_cost'] = total_maintenance_cost
        return context


class DashboardMaintenanceListView(ListView):
    template_name = 'car_rental/dashboard/maintenance_list.html'
    model = CarMaintenance
    paginate_by = 10
    ordering = 'date_of_repair'
