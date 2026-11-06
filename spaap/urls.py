from django.urls import path
from . import views
from .views import crea_Cita  # <-- Importamos la función con su nombre real

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios_view, name='servicios'),
    path('citas/', views.lista_citas, name='citas'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('crea/', crea_Cita, name="crea_Cita"),  # <-- Apunta a crea_Cita
    path('editar/<int:pk>/', views.editar_cita, name="editar_cita"),
    path('eliminar/<int:pk>/', views.eliminar_cita, name="eliminar_cita"),
    path('mapa/', views.mapa, name='mapa'),
    path('registro/', views.registrar_cliente, name='registrar_cliente'),
    path('buscar/', views.buscar_Cita, name='buscar_Cita'),

]


