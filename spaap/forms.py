from django import forms
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