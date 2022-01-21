
from django import forms
from .models import User

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
        

#Formulario que no se base en un modelo
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
    
    
