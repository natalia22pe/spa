import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CitaForm, ClienteForm, RegistroForm
from .models import Cita, Cliente, Local


# ==========================================
# AUTENTICACIÓN Y SEGURIDAD (3 INTENTOS Y ROLES)
# ==========================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if "intentos_login" not in request.session:
        request.session["intentos_login"] = 0

    if request.session["intentos_login"] >= 3:
        messages.error(request, "⚠️ Has superado los 3 intentos permitidos. Acceso bloqueado temporalmente.")
        return render(request, "spaap/login.html", {"form": AuthenticationForm(), "bloqueado": True})

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            request.session["intentos_login"] = 0  # Reinicia los intentos si entra bien
            user = form.get_user()
            login(request, user)

            siguiente = request.GET.get("next")
            if siguiente and url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):
                return redirect(siguiente)
            return redirect("inicio")
        else:
            request.session["intentos_login"] += 1
            intentos_restantes = 3 - request.session["intentos_login"]
            if intentos_restantes > 0:
                messages.error(request, f"Credenciales incorrectas. Te quedan {intentos_restantes} intentos.")
            else:
                messages.error(request, "⚠️ Has superado los 3 intentos permitidos. Acceso bloqueado.")
    else:
        form = AuthenticationForm()

    return render(request, "spaap/login.html", {"form": form})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario cifrando su contraseña
            
            # Mapeo del rol seleccionado en el formulario con los grupos del Admin
            rol_seleccionado = form.cleaned_data.get('rol', 'cliente')
            
            mapeo_grupos = {
                'Cliente': 'cliente',
                'Especialista': 'Especialista',
                'Administrador': 'Administrador',
                'cliente': 'cliente',
            }
            
            nombre_grupo = mapeo_grupos.get(rol_seleccionado, 'cliente')
            grupo = Group.objects.filter(name=nombre_grupo).first()
            if grupo:
                user.groups.add(grupo)

            messages.success(request, "¡Cuenta creada exitosamente! Por favor inicia sesión.")
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'spaap/registro.html', {'form': form})


# ==========================================
# VISTAS GENERALES Y ESTÁTICAS
# ==========================================

def inicio(request):
    # Limpiamos el contador de intentos fallidos al volver al inicio para facilitar las pruebas
    if "intentos_login" in request.session:
        request.session["intentos_login"] = 0
    return render(request, "spaap/index.html")

def servicios_view(request):
    return render(request, "spaap/servicios.html")


def contacto_view(request):
    return render(request, "spaap/contacto.html")


# ==========================================
# GESTIÓN DE CLIENTES
# ==========================================

def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente registrado correctamente.")
            return redirect('crea_Cita')
    else:
        form = ClienteForm()
    return render(request, 'spaap/registros_cliente.html', {'form': form})


# ==========================================
# CONTROL DE PERMISOS (ADMIN / ESPECIALISTA)
# ==========================================

def es_admin_o_especialista(user):
    return user.is_authenticated and user.groups.filter(name__in=['Administrador', 'Especialista']).exists()


# ==========================================
# CRUD DE CITAS (Con Seguridad y Privacidad de Roles)
# ==========================================

@login_required(login_url='login')
@user_passes_test(es_admin_o_especialista, login_url='inicio')
def lista_citas(request):
    citas = Cita.objects.all()
    return render(request, "spaap/citas.html", {"citas": citas})


def crea_Cita(request):
    url = "https://date.nager.at/api/v3/PublicHolidays/2026/CO"
    response = requests.get(url)

    fechas_festivas = []
    if response.status_code == 200:
        fechas_festivas = response.json()

    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita registrada correctamente")
            return redirect('crea_Cita')
    else:
        form = CitaForm()

    context = {"form": form, "festivos": fechas_festivas}
    return render(request, "spaap/reserva.html", context)


@login_required(login_url='login')
@user_passes_test(es_admin_o_especialista, login_url='inicio')
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    form = CitaForm(request.POST or None, instance=cita)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Editado de manera correcta")
        return redirect("citas")

    nombre_cliente = f"{cita.cliente_rel.nombre}" if cita.cliente_rel else "Sin cliente"

    return render(
        request,
        "spaap/editar.html",
        {"form": form, "titulo": f"Editar Cita de {nombre_cliente}"},
    )


@login_required(login_url='login')
@user_passes_test(es_admin_o_especialista, login_url='inicio')
def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == "POST":
        cita.delete()
        return redirect("citas")
    return render(request, "spaap/eliminar.html", {"cita": cita})


# ==========================================
# BÚSQUEDA Y MAPA DE LOCALES
# ==========================================

@login_required(login_url='login')
@user_passes_test(es_admin_o_especialista, login_url='inicio')
def buscar_Cita(request):
    query = request.GET.get('nombre', '').strip()
    citas = []

    if query:
        citas = Cita.objects.filter(cliente_rel__nombre__icontains=query)

    return render(
        request, 'spaap/citas.html', {'citas': citas, 'query': query}
    )


def mapa(request):
    locales_qs = Local.objects.all()

    query = request.GET.get("q", "")
    if query:
        locales_qs = locales_qs.filter(nombre__icontains=query) | locales_qs.filter(
            direccion__icontains=query
        )

    locales_list = []
    for loc in locales_qs:
        if loc.lat is not None and loc.lng is not None:
            locales_list.append({
                "nombre": loc.nombre,
                "direccion": loc.direccion,
                "lat": float(loc.lat),
                "lng": float(loc.lng),
            })

    contexto = {
        "locales_qs": locales_qs,
        "locales": json.dumps(locales_list),
    }
    return render(request, "spaap/mapa.html", contexto)