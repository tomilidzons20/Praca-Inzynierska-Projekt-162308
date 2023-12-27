from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django_filters.views import FilterView

from .filters import MaintenanceFilter
from .forms import CarForm
from .forms import CarMaintenanceForm
from .forms import CarRentalForm
from .models import Car
from .models import CarMaintenance
from .models import CarRental


class DashboardHomeView(TemplateView):
    template_name = 'car_rental/dashboard/home.html'


class DashboardCarListView(ListView):
    template_name = 'car_rental/dashboard/car_list.html'
    model = Car
    paginate_by = 10
    ordering = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_form'] = CarForm
        return context


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
    paginate_by = 10
    ordering = 'date_of_repair'
    filterset_class = MaintenanceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintenance_form'] = CarMaintenanceForm
        return context


class DashboardRentalListView(ListView):
    template_name = 'car_rental/dashboard/rental_list.html'
    model = CarRental
    paginate_by = 10
    ordering = 'end_date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental_form'] = CarRentalForm
        return context


def maintenance_create_view(request):
    if request.method == 'POST':
        form = CarMaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_maintenance_list')


def car_create_view(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_car_list')


def rental_create_view(request):
    if request.method == 'POST':
        form = CarRentalForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_rental_list')
