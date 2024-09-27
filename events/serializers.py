from rest_framework import serializers
from events.models import Event
from datetime import date


class DefaultSerializer(serializers.Serializer):
    """
    Este serializador se utiliza como serializador por defecto.
    No contiene ninguna regla de negocio.
    Solo se utiliza para devolver una respuesta vacía en caso de que no se haya definido un serializador específico para una acción.
    """

    pass


class CreateEventSerializer(serializers.Serializer):
    """
    Este serializador se utiliza para la creación o actualización de eventos.
    Contiene las reglas de negocio para validar los campos de entrada de forma individual y en conjunto (en el caso de las fechas de inicio y fin).
    """

    name = serializers.CharField(max_length=255)
    start = serializers.DateField()
    end = serializers.DateField()
    total_tickets = serializers.IntegerField()

    def validate_start(self, value) -> date:
        """
        Valida que la fecha de inicio sea mayor o igual que la fecha actual
        """
        if value < date.today():
            raise serializers.ValidationError(
                "La fecha de inicio no puede estar en el pasado"
            )
        return value

    def validate_end(self, value) -> date:
        """
        Valida que la fecha de fin sea mayor que la fecha actual
        """
        if value < date.today():
            raise serializers.ValidationError(
                "La fecha de fin no puede estar en el pasado"
            )
        return value

    def validate_total_tickets(self, value) -> int:
        """
        Valida que el número total de boletos sea mayor que 0 y menor o igual a 300.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "El número total de boletos debe ser mayor que 0"
            )
        if value > 300:
            raise serializers.ValidationError(
                "El número total de boletos no puede ser mayor a 300"
            )
        return value

    def validate(self, attrs) -> dict:
        """
        Valida que la fecha de inicio sea menor que la fecha de fin.
        """
        if attrs["start"] > attrs["end"]:
            raise serializers.ValidationError(
                {"start": "La fecha de inicio no puede ser mayor que la fecha de fin"}
            )
        return attrs


class ListEventSerializer(serializers.Serializer):
    """
    Este serializador se utiliza para listar eventos.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    start = serializers.DateField()
    end = serializers.DateField()
    total_tickets = serializers.IntegerField()


class RetrieveEventSerializer(serializers.Serializer):
    """
    Este serializador se utiliza para mostrar un evento específico.
    Calcula el número total de boletos vendidos y canjeados.
    Los campos 'total_sold_tickets' y 'total_redeemed_tickets' son solo de lectura y calculados en base a los boletos asociados al evento.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    start = serializers.DateField()
    end = serializers.DateField()
    total_tickets = serializers.IntegerField()
    total_sold_tickets = serializers.IntegerField()
    total_redeemed_tickets = serializers.IntegerField()


class TicketSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    event = serializers.CharField(source="event.name")
    redeemed = serializers.BooleanField()
