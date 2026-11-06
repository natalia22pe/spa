from django.contrib import admin
from .models import Local, Cita, Cliente, Especialista, Servicio  

admin.site.register(Servicio)
admin.site.register(Especialista)
admin.site.register(Cliente)
admin.site.register(Cita)   
admin.site.register(Local)


