from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic import (
    View, 
    CreateView
)
from django.views.generic.edit import FormView

from .forms import (
    UserRegisterForm, 
    LoginForm, 
    UpdatePasswordForm,
    VerificationForm
)
from .models import User
from .function import code_generator

# Create your views here.
#Registrar un usuario
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '.'

    def form_valid(self, form):
        #Generamos el codigo
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            #extra_fields
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo
        )

        #Enviar codigo a email de usuario
        asunto = "Confirmacion de email"
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente = "omarjunior041204@gmail.com"
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'], ])

        #Redirigir a la pantalla de validacion
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs = {'pk': usuario.id}
            )
        )


#Logeo de usuario
class LoginUser(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home_app:user-panel')

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


#Actualizar el password del usuario
class UpdatedPassword(LoginRequiredMixin, FormView):
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    #Por si la contraseña actual no es la correcta
    login_url = reverse_lazy('users_app:user-login') 

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2'] 
            user.set_password(new_password)
            user.save() 

        logout(self.request)
        return super().form_valid(form)


#Verificacion del codigo
class CodeVerificationView(FormView):
    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        #
        User.objects.filter(pk = self.kwargs['pk']).update(is_active = True)
        return super().form_valid(form)


