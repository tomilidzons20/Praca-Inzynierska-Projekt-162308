from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import AddressForm
from .forms import ProfileForm
from .models import Address
from .models import CustomUser


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'account/profile.html'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address, _ = Address.objects.get_or_create(account=self.request.user)
        context['address_form'] = AddressForm(instance=address)
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
