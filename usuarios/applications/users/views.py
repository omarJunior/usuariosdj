from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.views.generic import (
    View, 
    CreateView
)
from django.views.generic.edit import FormView

from .forms import UserRegisterForm, LoginForm
from .models import User

# Create your views here.
#Registrar un usuario
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '.'

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
        )
        return super().form_valid(form)


#Logeo de usuario
class LoginUser(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
        return super().form_valid(form)


#Cerrar sesion
class LogoutView(View):
    #request - contexto del navegador
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )



