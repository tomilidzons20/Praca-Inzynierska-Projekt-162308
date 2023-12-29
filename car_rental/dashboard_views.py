from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django_filters.views import FilterView

from .filters import MaintenanceFilter
from .filters import ContactFilter
from .filters import CarRentalFilter
from .forms import CarForm
from .forms import CarMaintenanceForm
from .forms import CarRentalForm
from .forms import ContactForm
from .forms import RentalProtectionForm
from .forms import RentalExtraForm
from .forms import NewsForm
from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .models import ContactMessage
from .models import RentalProtection
from .models import RentalExtra
from .models import News


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


class DashboardRentalListView(FilterView):
    template_name = 'car_rental/dashboard/rental_list.html'
    model = CarRental
    paginate_by = 10
    ordering = 'end_date'
    filterset_class = CarRentalFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental_form'] = CarRentalForm
        return context


class DashboardContactListView(FilterView):
    template_name = 'car_rental/dashboard/contact_list.html'
    model = ContactMessage
    paginate_by = 10
    filterset_class = ContactFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm
        return context


class DashboardRentalProtectionListView(ListView):
    template_name = 'car_rental/dashboard/rental_protection_list.html'
    model = RentalProtection
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protection_form'] = RentalProtectionForm
        return context


class DashboardRentalExtraListView(ListView):
    template_name = 'car_rental/dashboard/rental_extra_list.html'
    model = RentalExtra
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_form'] = RentalExtraForm
        return context


class DashboardNewsListView(ListView):
    template_name = 'car_rental/dashboard/news_list.html'
    model = News
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_form'] = NewsForm
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


def contact_create_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_contact_list')


def rental_protection_create_view(request):
    if request.method == 'POST':
        form = RentalProtectionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_protection_list')


def rental_extra_create_view(request):
    if request.method == 'POST':
        form = RentalExtraForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_extra_list')


def news_create_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_news_list')

# TODO
# rest of dashboard views | crud
# update: contact, news, rental protection, rental extra


