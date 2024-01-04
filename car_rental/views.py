from math import ceil

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _gettext
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from .forms import CarAddressForm
from .forms import CarChoiceForm
from .forms import CarDaysRentalForm
from .forms import CarExtraForm
from .forms import ClientContactForm
from .forms import RentalReviewForm
from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .models import ContactMessage
from .models import News
from .models import RentalAddress


class HomeView(TemplateView):
    template_name = 'car_rental/main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = News.objects.all().order_by('-add_date')[:3]
        context['lowest_car_cost'] = Car.objects.all().order_by('day_cost').first().day_cost
        return context


class NewsListView(ListView):
    model = News
    template_name = 'car_rental/main/news.html'

    def get_queryset(self):
        return News.objects.all().order_by('-add_date')


class NewsDetailView(DetailView):
    model = News
    template_name = 'car_rental/main/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_news'] = News.objects.filter(
            add_date__lt=self.object.add_date
        ).order_by('-add_date').first()
        context['next_news'] = News.objects.filter(
            add_date__gt=self.object.add_date
        ).order_by('add_date').first()
        return context


class CarRentalForDaysView(LoginRequiredMixin, SessionWizardView):
    form_list = [
        ('days', CarDaysRentalForm),
        ('car', CarChoiceForm),
        ('extra', CarExtraForm),
        ('address', CarAddressForm),
        ('review', RentalReviewForm),
    ]
    template_list = {
        'days': 'car_rental/main/car_rental_days/date_range.html',
        'car': 'car_rental/main/car_rental_days/car_choice.html',
        'extra': 'car_rental/main/car_rental_days/extra_choice.html',
        'address': 'car_rental/main/car_rental_days/address.html',
        'review': 'car_rental/main/car_rental_days/review.html',
    }

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step)
        if step == 'address':
            kwargs['request'] = self.request
        return kwargs

    def calculate_total_cost(self, date_to, date_from, car, protection, extra):
        rental_days = ceil(((date_to - date_from).total_seconds() / 3600) / 24)
        extras_cost = sum([extra.cost for extra in extra])
        return protection.cost + extras_cost + car.day_cost * rental_days

    def get_address_data(self):
        first_name = self.get_cleaned_data_for_step('address')['first_name']
        last_name = self.get_cleaned_data_for_step('address')['last_name']
        building_number = self.get_cleaned_data_for_step('address')['building_number']
        post_code = self.get_cleaned_data_for_step('address')['post_code']
        city = self.get_cleaned_data_for_step('address')['city']
        street = self.get_cleaned_data_for_step('address')['street']
        address = {
            'first_name': first_name,
            'last_name': last_name,
            'building_number': building_number,
            'post_code': post_code,
            'city': city,
            'street': street,
        }
        return address

    def get_template_names(self):
        return [self.template_list[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'car':
            date_from = self.get_cleaned_data_for_step('days')['date_from']
            date_to = self.get_cleaned_data_for_step('days')['date_to']
            rental_days = ceil(((date_to - date_from).total_seconds() / 3600) / 24)
            context.update({'days': rental_days})
        if self.steps.current == 'review':
            date_from = self.get_cleaned_data_for_step('days')['date_from']
            date_to = self.get_cleaned_data_for_step('days')['date_to']
            car = self.get_cleaned_data_for_step('car')['car']
            protection = self.get_cleaned_data_for_step('extra')['protection']
            extra = self.get_cleaned_data_for_step('extra')['extra']
            use_profile_address = self.get_cleaned_data_for_step('address')['use_profile_address']
            if use_profile_address:
                address = self.request.user.address
            else:
                address = self.get_address_data()

            rental_days = ceil(((date_to - date_from).total_seconds() / 3600) / 24)
            total_cost = self.calculate_total_cost(date_to, date_from, car, protection, extra)
            context.update({
                'date_from': date_from,
                'date_to': date_to,
                'days': rental_days,
                'car': car,
                'protection': protection,
                'extra': extra,
                'address': address,
                'total_cost': total_cost,
            })

        return context

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if step is None:
            step = self.steps.current
        if step == 'car':
            date_from = self.get_cleaned_data_for_step('days')['date_from']
            date_to = self.get_cleaned_data_for_step('days')['date_to']

            all_cars = Car.objects.filter(
                ~Q(status=Car.StatusChoices.UNAVAILABLE)
            )
            available_cars = []
            for car in all_cars:
                # if rentals already exist or maintenance scheduled or is in repair
                # during selected period look for another car
                car_rentals = CarRental.objects.filter(
                    Q(status=CarRental.StatusChoices.RESERVED) |
                    Q(status=CarRental.StatusChoices.RENTED),
                    Q(start_date__lte=date_from, end_date__gte=date_from) |
                    Q(start_date__lte=date_to, end_date__gte=date_to) |
                    Q(start_date__gte=date_from, start_date__lte=date_to) &
                    Q(end_date__gte=date_from, end_date__lte=date_to),
                    car=car.id,
                )
                if car_rentals:
                    continue
                car_maintenance = CarMaintenance.objects.filter(
                    Q(status=CarMaintenance.MaintenanceChoices.SCHEDULED) |
                    Q(status=CarMaintenance.MaintenanceChoices.INREPAIR),
                    date_of_repair__gte=date_from,
                    date_of_repair__lte=date_to,
                    car=car,
                )
                if car_maintenance:
                    continue
                available_cars.append(car.id)
            form.fields['car'].queryset = Car.objects.filter(
                id__in=available_cars
            ).order_by('id')
        return form

    def done(self, form_list, form_dict, **kwargs):
        date_from = self.get_cleaned_data_for_step('days')['date_from']
        date_to = self.get_cleaned_data_for_step('days')['date_to']
        car = self.get_cleaned_data_for_step('car')['car']
        protection = self.get_cleaned_data_for_step('extra')['protection']
        extra = self.get_cleaned_data_for_step('extra')['extra']

        total_cost = self.calculate_total_cost(date_to, date_from, car, protection, extra)

        use_profile_address = self.get_cleaned_data_for_step('address')['use_profile_address']

        if use_profile_address:
            user_address = self.request.user.address
            if not hasattr(self.request.user, 'address'):
                message = _gettext("You don't have saved address in profile")
                return render(
                    self.request,
                    'car_rental/main/car_rental_days/rental_unsuccessful.html',
                    context={'error': message}
                )
            address, _ = RentalAddress.objects.get_or_create(
                user=user_address.account,
                first_name=user_address.first_name,
                last_name=user_address.last_name,
                street=user_address.street,
                building_number=user_address.building_number,
                post_code=user_address.post_code,
                city=user_address.city,
            )
        else:
            address_data = self.get_address_data()
            address, _ = RentalAddress.objects.get_or_create(
                user=self.request.user,
                first_name=address_data['first_name'],
                last_name=address_data['last_name'],
                street=address_data['street'],
                building_number=address_data['building_number'],
                post_code=address_data['post_code'],
                city=address_data['city'],
            )

        car_rental = CarRental.objects.create(
            user=self.request.user,
            address=address,
            car=car,
            protection=protection,
            start_date=date_from,
            end_date=date_to,
            total_cost=total_cost,
            status=CarRental.StatusChoices.RESERVED,
        )
        car_rental.extra.add(*extra)

        return render(self.request, 'car_rental/main/car_rental_days/rental_successful.html')


class ContactCreateView(CreateView):
    model = ContactMessage
    form_class = ClientContactForm
    template_name = 'car_rental/main/contact.html'

    def form_valid(self, form):
        message = form.save(commit=False)
        message.user = self.request.user
        message.add_date = timezone.now()
        message.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contact')
