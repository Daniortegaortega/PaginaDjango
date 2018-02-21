from django.forms import ModelForm
from django import forms
from captcha.fields import ReCaptchaField
from Liga.models import Adicional,User

class registrar(forms.Form):
    username= forms.CharField(min_length=2, max_length=20)
    email= forms.EmailField(max_length=50)
    password = forms.CharField(max_length=10, widget=forms.PasswordInput)
    nombre = forms.CharField(min_length=2, max_length=30)
    apellidos = forms.CharField(min_length=2,max_length=50)
    telefono = forms.CharField(max_length=9,min_length=9)
    numero_cuenta= forms.CharField(max_length=10, min_length=10)
    foto = forms.ImageField()
    captcha = ReCaptchaField()


    def clean_username(self):
        u= User.objects.all()
        for x in u:
            if x.username == self.cleaned_data['username']:
                raise forms.ValidationError("El nombre de usuario ya esta en uso")
        return self.cleaned_data['username']

    def clean_telefono(self):
        if len(self.cleaned_data['telefono']) != 9:
            raise forms.ValidationError("Debe estar compuesto de 9 numeros")
        elif self.cleaned_data['telefono'].isdigit()==False:
            raise forms.ValidationError("Solo puede contener numeros")
        return self.cleaned_data['telefono']

    def clean_numero_cuenta(self):
        a= Adicional.objects.all()
        for x in a:
            if x.numero_cuenta == self.cleaned_data['numero_cuenta']:
                raise forms.ValidationError("El numero de cuenta ya existe en la bd")
        if self.cleaned_data['numero_cuenta'][0:2]!="ES":
            raise forms.ValidationError("El numero de cuenta debe empezar por ES")
        elif self.cleaned_data['numero_cuenta'][2:10].isdigit()==False:
            raise forms.ValidationError("El numero de cuenta debe empezar por ES, seguido de 8 numeros")
        elif len(self.cleaned_data['numero_cuenta'])<10:
            raise forms.ValidationError("La longitud del numero de cuentas es de 8 Digitos")
        return self.cleaned_data['numero_cuenta']

    def clean(self):
        cleaned_data=self.cleaned_data
        return cleaned_data

class username(forms.Form):
    old_username = forms.CharField(max_length=15,label="Actual username")
    new_username = forms.CharField(max_length=15, label="Nuevo username")

    def clean_new_username(self):
        u = User.objects.all()
        for x in u:
            if x.username == self.cleaned_data['new_username']:
                raise forms.ValidationError("Nombre de usuario ya en uso")

    def clean(self):
        cleaned_data=self.cleaned_data
        return cleaned_data

class Saldo(ModelForm):
    class Meta:
        model = Adicional
        fields = ('numero_cuenta', 'saldo')
        labels = {
            'numero_cuenta': ('Numero de cuenta bancaria')
        }
        help_texts = {
            'numero_cuenta': ('IBAN: ESXXXXXXXX')
        }
        error_messages = {
            'numero_cuenta': {
                'max_length': ('Numero de cuenta muy largo, solo 10 caracteres')
            }
        }

    def clean_numero_cuenta(self):
        if self.cleaned_data['numero_cuenta'][0:2]!="ES":
            raise forms.ValidationError("El numero de cuenta debe empezar por ES")
        elif self.cleaned_data['numero_cuenta'][2:10].isdigit()==False:
            raise forms.ValidationError("El numero de cuenta debe empezar por ES, seguido de 8 numeros")
        elif len(self.cleaned_data['numero_cuenta'])<10:
            raise forms.ValidationError("La longitud del numero de cuentas es de 8 Digitos")
        return self.cleaned_data['numero_cuenta']

    def clean_saldo(self):
        if self.cleaned_data['saldo']<0:
            raise forms.ValidationError("El saldo no puede ser negativo")
        return self.cleaned_data['saldo']

    def clean(self):
        cleaned_data=self.cleaned_data
        return cleaned_data


class contactar(forms.Form):
    correo = forms.EmailField()
    asunto = forms.CharField(max_length=25)
    mensaje = forms.CharField(max_length=100)





