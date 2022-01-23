
from django import forms
from .models import User
from django.contrib.auth import authenticate

class UserRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label= 'Contraseña',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label= 'Contraseña',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'Repetir contraseña'
            }
        )
    )

    class Meta:
        model = User
        #Datos que se me mostraran en el formulario
        fields = ('username', 'email', 'nombres', 'apellidos', 'genero')

    #Validacion del formulario
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            self.add_error('password2', 'Las contraseñas no son las mismas')
            if len(password1) <= 3 and len(password2) <= 3:
                self.add_error('password2', 'Las contraseñas deben ser mayor a 3 caracteres')
        

#Formulario que no se basa en un modelo
class LoginForm(forms.Form):
    """LoginForm definition."""
    
    username = forms.CharField(
        label= 'Username',
        required= True,
        widget= forms.TextInput(
            attrs = {
                'placeholder': 'Username',
                'style': '{margin: 10px}',
            }
        )
    )

    password = forms.CharField(
        label= 'Contraseña',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'Contraseña',
                'style': '{margin: 10px}',
            }
        )
    )

    #Validacion del formulario de login
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username = username, password = password):
            raise forms.ValidationError('Los datos del usuario no son correctos')
        return cleaned_data
        
            
        
class UpdatePasswordForm(forms.Form):
    
    password1 = forms.CharField(
        label= 'Contraseña',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'Contraseña actual',
                'style': '{margin: 10px}',
            }
        )
    )
    password2 = forms.CharField(
        label= 'Contraseña',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'Contraseña nueva',
                'style': '{margin: 10px}',
            }
        )
    )


class VerificationForm(forms.Form):
    codregistro = forms.CharField(
        label= 'Codigo confirmacion',
        required= True
    )    
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']
        if len(codigo) == 6:
            #Verificamos si el codigo y el id del usuario son validos
            activo = User.objects.cod_validation(self.id_user, codigo)
            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')
        else:
            raise forms.ValidationError('El codigo es incorrecto')
            
