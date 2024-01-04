from django.contrib.admin.views.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import UpdateView
from django_filters.views import FilterView

from .filters import CarRentalFilter
from .filters import ContactFilter
from .filters import MaintenanceFilter
from .filters import NewsFilter
from .forms import CarForm
from .forms import CarMaintenanceForm
from .forms import CarMaintenanceUpdateForm
from .forms import CarRentalForm
from .forms import CarRentalUpdateForm
from .forms import ContactForm
from .forms import NewsForm
from .forms import RentalExtraForm
from .forms import RentalProtectionForm
from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .models import ContactMessage
from .models import News
from .models import RentalExtra
from .models import RentalProtection


def is_staff(user):
    return user.is_superuser or user.is_staff


class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('account_login')


class DashboardCarListView(StaffRequiredMixin, ListView):
    template_name = 'car_rental/dashboard/car/car_list.html'
    model = Car
    paginate_by = 10
    ordering = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_form'] = CarForm
        return context


class DashboardCarUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'car_rental/dashboard/car/car_update.html'
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


class DashboardMaintenanceListView(StaffRequiredMixin, FilterView):
    template_name = 'car_rental/dashboard/maintenance/maintenance_list.html'
    model = CarMaintenance
    paginate_by = 10
    ordering = 'date_of_repair'
    filterset_class = MaintenanceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintenance_form'] = CarMaintenanceForm
        return context


class DashboardMaintenanceUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'car_rental/dashboard/maintenance/maintenance_update.html'
    model = CarMaintenance
    form_class = CarMaintenanceUpdateForm

    def get_success_url(self):
        return reverse_lazy('dashboard_maintenance_update', kwargs={'pk': self.object.id})


class DashboardRentalListView(StaffRequiredMixin, FilterView):
    template_name = 'car_rental/dashboard/rental/rental_list.html'
    model = CarRental
    paginate_by = 10
    ordering = 'end_date'
    filterset_class = CarRentalFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental_form'] = CarRentalForm
        return context


class DashboardRentalUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'car_rental/dashboard/rental/rental_update.html'
    model = CarRental
    form_class = CarRentalUpdateForm

    def get_success_url(self):
        return reverse_lazy('dashboard_rental_update', kwargs={'pk': self.object.id})


class DashboardContactListView(StaffRequiredMixin, FilterView):
    template_name = 'car_rental/dashboard/contact/contact_list.html'
    model = ContactMessage
    paginate_by = 10
    filterset_class = ContactFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm
        return context


class DashboardContactUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'car_rental/dashboard/contact/contact_update.html'
    model = ContactMessage
    form_class = ContactForm

    def get_success_url(self):
        return reverse_lazy('dashboard_contact_update', kwargs={'pk': self.object.id})


class DashboardRentalProtectionListView(StaffRequiredMixin, ListView):
    template_name = 'car_rental/dashboard/rental_protection/rental_protection_list.html'
    model = RentalProtection
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protection_form'] = RentalProtectionForm
        return context


class DashboardRentalProtectionUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'car_rental/dashboard/rental_protection/rental_protection_update.html'
    model = RentalProtection
    form_class = RentalProtectionForm

    def get_success_url(self):
        return reverse_lazy('dashboard_protection_update', kwargs={'pk': self.object.id})


class DashboardRentalExtraListView(StaffRequiredMixin, ListView):
    template_name = 'car_rental/dashboard/rental_extra/rental_extra_list.html'
    model = RentalExtra
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_form'] = RentalExtraForm
        return context


class DashboardRentalExtraUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'car_rental/dashboard/rental_extra/rental_extra_update.html'
    model = RentalExtra
    form_class = RentalExtraForm

    def get_success_url(self):
        return reverse_lazy('dashboard_extra_update', kwargs={'pk': self.object.id})


class DashboardNewsListView(StaffRequiredMixin, FilterView):
    template_name = 'car_rental/dashboard/news/news_list.html'
    model = News
    paginate_by = 10
    filterset_class = NewsFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_form'] = NewsForm
        return context


class DashboardNewsUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'car_rental/dashboard/news/news_update.html'
    model = News
    form_class = NewsForm

    def get_success_url(self):
        return reverse_lazy('dashboard_news_update', kwargs={'pk': self.object.id})


@user_passes_test(is_staff)
def maintenance_create_view(request):
    if request.method == 'POST':
        form = CarMaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_maintenance_list')


@user_passes_test(is_staff)
def car_create_view(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_car_list')


@user_passes_test(is_staff)
def rental_create_view(request):
    if request.method == 'POST':
        form = CarRentalForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_rental_list')


@user_passes_test(is_staff)
def contact_create_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_contact_list')


@user_passes_test(is_staff)
def rental_protection_create_view(request):
    if request.method == 'POST':
        form = RentalProtectionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_protection_list')


@user_passes_test(is_staff)
def rental_extra_create_view(request):
    if request.method == 'POST':
        form = RentalExtraForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_extra_list')


@user_passes_test(is_staff)
def news_create_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('dashboard_news_list')
