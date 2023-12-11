from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django_filters.views import FilterView

from .forms import CarForm
from .forms import CarRentalForm
from .forms import CarMaintenanceForm
from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .filters import MaintenanceFilter


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
        context['maintenance_form'] = CarMaintenanceForm
        return context


class DashboardMaintenanceListView(FilterView):
    template_name = 'car_rental/dashboard/maintenance_list.html'
    model = CarMaintenance
    # paginate_by = 10
    ordering = 'date_of_repair'
    filterset_class = MaintenanceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['maintenance_form'] = CarMaintenanceForm
        return context


class DashboardRentalListView(ListView):
    template_name = 'car_rental/dashboard/rental_list.html'
    model = CarRental
    ordering = 'end_date'


class DashboardRentalCreateView(CreateView):
    template_name = 'car_rental/dashboard/rental_create.html'
    model = CarRental
    form_class = CarRentalForm

    def get_success_url(self):
        return reverse_lazy('dashboard_rental_list')