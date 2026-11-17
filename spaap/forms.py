from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cita, Cliente


class CitaForm(forms.ModelForm):

  class Meta:
    model = Cita
    fields = [
        "fecha_hora",
        "estado",
        "notas",
        "cliente_rel",
        "servicio_rel",
        "especialista_rel",
    ]


class ClienteForm(forms.ModelForm):

  class Meta:
    model = Cliente
    fields = ["nombre", "documento", "telefono"]


class RegistroForm(UserCreationForm):
    ROLES_CHOICES = [
        ('cliente', 'Cliente'),
        ('Especialista', 'Especialista'),
        ('Administrador', 'Administrador'),
    ]
    rol = forms.ChoiceField(
        choices=ROLES_CHOICES, 
        label="Selecciona tu Rol", 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']