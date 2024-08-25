from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from .forms import *

from .models import Car, Maker


# Create your views here.
class CarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'Main/cars.html'
    context_object_name = 'cars'
    
    def get_queryset(self):
        maker = self.request.GET.get("maker")
        search = self.request.GET.get("search")
        cars = Car.objects.select_related('maker', 'owner')
        if maker is not None and len(maker) > 0:
            cars = cars.filter(maker__name=maker)

        if search is not None and len(search) > 0:
            cars = cars.filter(Q(car_model__icontains=search) | Q(comments__icontains=search))
        return cars

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = "cars"
        context['title'] = "Add a car"
        context['action'] = "create"
        context['makers'] = Maker.objects.all()

        return context


class MakerListView(LoginRequiredMixin, ListView):
    model = Maker
    template_name = 'Main/makers.html'
    context_object_name = 'makers'


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'form.html'
    success_url = reverse_lazy('cars')

    def form_valid(self, form):
        # Set the user field to the current user before saving
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = "cars"
        context['title'] = "Add a car"
        context['action'] = "create"

        return context


class MakerCreateView(LoginRequiredMixin, CreateView):
    model = Maker
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('makers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = "makers"
        context['title'] = "Add a maker"
        context['action'] = "Add"
        return context


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)

        return response

    def get_success_url(self):
        # Retrieve the 'next' query parameter from the request
        next_url = self.request.GET.get('next')

        # If 'next' is provided, use it; otherwise, use a default URL
        if next_url:
            return next_url
        else:
            return reverse('main')  # Fallback URL if 'next' is not provided


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = 'form.html'
    success_url = reverse_lazy("cars")
    form_class = CarForm

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        # Set the user field to the current user before saving
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = "cars"
        context['title'] = "Edit a car"
        context['action'] = "Apply changes"
        return context


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'form.html'
    success_url = reverse_lazy("cars")

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = "cars"
        context['title'] = f"Are you sure you want to delete this car ?"
        context['action'] = "Delete"
        return context


class MakerDeleteView(LoginRequiredMixin, DeleteView):
    model = Maker
    template_name = 'form.html'
    success_url = reverse_lazy("cars")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = "makers"
        context['title'] = f"Are you sure you want to delete the maker : '{self.kwargs.get('name')}' ?"
        context['action'] = "Delete"
        return context

    def get_object(self, *args, **kwargs):
        name = self.kwargs.get('name')
        return get_object_or_404(Maker, name=name)
