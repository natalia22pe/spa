# from django.urls import path
# from . import views
# from .views import crea_Cita  # <-- Importamos la función con su nombre real

# urlpatterns = [
#     path('', views.inicio, name='inicio'),
#     path('servicios/', views.servicios_view, name='servicios'),
#     path('citas/', views.lista_citas, name='citas'),
#     path('contacto/', views.contacto_view, name='contacto'),
#     path('crea/', crea_Cita, name="crea_Cita"),  # <-- Apunta a crea_Cita
#     path('editar/<int:pk>/', views.editar_cita, name="editar_cita"),
#     path('eliminar/<int:pk>/', views.eliminar_cita, name="eliminar_cita"),
#     path('mapa/', views.mapa, name='mapa'),
#     path('registro/', views.registrar_cliente, name='registrar_cliente'),
#     path('buscar/', views.buscar_Cita, name='buscar_Cita'),

# ]


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import crea_Cita  # <-- Importamos la función con su nombre real

urlpatterns = [
    # Rutas principales y estáticas
    path('', views.inicio, name='inicio'),  # <--- Cambiamos 'index' por 'inicio'
    path('servicios/', views.servicios_view, name='servicios'),
    path('contacto/', views.contacto_view, name='contacto'),

    # Rutas de Autenticación y Seguridad
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),

    # Rutas de Citas y CRUD
    path('citas/', views.lista_citas, name='citas'),
    path('crea/', crea_Cita, name="crea_Cita"),
    path('editar/<int:pk>/', views.editar_cita, name="editar_cita"),
    path('eliminar/<int:pk>/', views.eliminar_cita, name="eliminar_cita"),
    path('buscar/', views.buscar_Cita, name='buscar_Cita'),

    # Rutas de Clientes y Mapas
    path('clientes/', views.registrar_cliente, name='registrar_cliente'),  # <-- Cambiamos a 'registrar_cliente'
    path('mapa/', views.mapa, name='mapa'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
]