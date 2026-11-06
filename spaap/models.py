from django.db import models


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    duracion_minutos = models.IntegerField(default=60)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Especialista(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    # Cambiado a CharField para evitar problemas con números largos
    documento = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=50)  # ej. Manicura, Masajes, Faciales
    correo = models.EmailField(unique=True)
    # Cambiado a CharField para evitar problemas con números largos
    telefono = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.especialidad})"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(
        max_length=100, blank=True, null=True
    )  # Asegurado por si lo pide el formulario
    documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} - Doc: {self.documento}"


class Cita(models.Model):
    ESTADO_CHOICES = [
        ("P", "Pendiente"),
        ("C", "Confirmada"),
        ("X", "Cancelada"),
    ]

    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default="P")
    notas = models.CharField(max_length=200, null=True, blank=True)

    # Relaciones de Llave Foránea (ForeignKey)
    cliente_rel = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="citas_cliente",
        null=True,
        blank=True,
    )

    servicio_rel = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="citas_servicio",
        null=True,
        blank=True,
    )

    especialista_rel = models.ForeignKey(
        Especialista,
        on_delete=models.CASCADE,
        related_name="citas_especialista",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Cita el {self.fecha_hora} - Estado: {self.get_estado_display()}"


class Local(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    def __str__(self):
        return self.nombre