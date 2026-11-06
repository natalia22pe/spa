import json
import requests
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CitaForm, ClienteForm
from .models import Cita, Cliente, Local


# ==========================================
# VISTAS GENERALES Y ESTÁTICAS
# ==========================================

def inicio(request):
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
# CRUD DE CITAS (Con API de Días Festivos)
# ==========================================

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


def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == "POST":
        cita.delete()
        return redirect("citas")
    return render(request, "spaap/eliminar.html", {"cita": cita})


# ==========================================
# BÚSQUEDA Y MAPA DE LOCALES
# ==========================================

def buscar_Cita(request):
    query = request.GET.get('nombre', '').strip()
    citas = []

    if query:
        # Filtramos por el nombre del cliente relacionado usando icontains
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