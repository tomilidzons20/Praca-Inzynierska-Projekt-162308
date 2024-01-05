from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from car_rental.models import CarRental

from .forms import AddressForm
from .forms import ProfileForm
from .models import Address
from .models import CustomUser


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'account/profile/profile.html'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            address = Address.objects.get(account=self.request.user)
        except Address.DoesNotExist:
            address = None
        rentals = CarRental.objects.filter(user=self.request.user).order_by('-start_date')
        context['address_form'] = AddressForm(instance=address)
        context['rentals'] = rentals
        return context

    def get_object(self, queryset=CustomUser):
        return get_object_or_404(queryset, id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('view_profile')


def address_update_view(request):
    if request.method == 'POST':
        address, _ = Address.objects.get_or_create(account=request.user)
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)
    return redirect('view_profile')


def cancel_rental_view(request):
    if request.method == 'POST':
        try:
            rental_id = request.POST.get('id')
            rental = CarRental.objects.get(id=rental_id, user=request.user)
            rental.status = CarRental.StatusChoices.CANCELLED
            rental.save()
            return JsonResponse({'success': True}, status=200)
        except CarRental.DoesNotExist:
            return JsonResponse({'errors': 'Rental does not exist'}, status=400)
    return redirect('view_profile')
