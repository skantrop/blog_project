from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .models import User
from .forms import RegistrationForm


class RegisterView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index-page')
    success_message = 'success registered'

class SignInView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index-page')

def profile(request):
    return render(request, 'profile.html')

