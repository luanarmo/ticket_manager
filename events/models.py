from django.db import models
import uuid


class Event(models.Model):
    """
    Modelo que representa un evento.
    Se utiliza para almacenar la información de los eventos que se crean.
    Agrege los campos 'created_at' y 'updated_at' para llevar un registro de las fechas de creación y actualización.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    total_tickets = models.PositiveSmallIntegerField()

    @property
    def total_sold_tickets(self) -> int:
        return Ticket.objects.filter(event=self).count()

    @property
    def total_redeemed_tickets(self) -> int:
        return Ticket.objects.filter(event=self, redeemed=True).count()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    """
    Modelo que representa un boleto.
    Se utiliza para almacenar la información de los boletos que se venden y canjean para un evento.
    El campo 'id' es un identificador único para el boleto, es por eso que se utiliza el tipo UUID4.
    El campo 'redeemed' indica si el boleto ha sido canjeado o no.
    Agrege los campos 'created_at' y 'updated_at' para llevar un registro de las fechas de creación y actualización.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    redeemed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
