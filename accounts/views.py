from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'account/profile.html'
    form_class = ProfileForm

    def get_object(self, queryset=CustomUser):
        return get_object_or_404(queryset, id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('view_profile')
