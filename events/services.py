from .models import Event, Ticket
from datetime import date
from graphql import GraphQLError


def validate_start(value: date) -> date:
    """
    Valida que la fecha de inicio sea mayor o igual que la fecha actual
    """
    if not value:
        return value

    if value < date.today():
        raise GraphQLError("La fecha de inicio no puede estar en el pasado")
    return value


def validate_end(value: date) -> date:
    """
    Valida que la fecha de fin sea mayor que la fecha actual
    """
    if not value:
        return value

    if value < date.today():
        raise GraphQLError("La fecha de fin no puede estar en el pasado")
    return value


def validate_total_tickets(value: int) -> int:
    """
    Valida que el número total de boletos sea mayor que 0 y menor o igual a 300.
    """
    if not value:
        return value

    if value <= 0:
        raise GraphQLError("El número total de boletos debe ser mayor que 0")
    if value > 300:
        raise GraphQLError("El número total de boletos no puede ser mayor a 300")
    return value


def validate_start_end(start: date, end: date) -> dict:
    """
    Valida que la fecha de inicio sea menor que la fecha de fin.
    """
    if not start or not end:
        return {"start": start, "end": end}

    if start > end:
        raise GraphQLError("La fecha de inicio no puede ser mayor que la fecha de fin")
    return {"start": start, "end": end}


def validate_all_fields(**kwargs) -> dict:
    """
    Valida que todos los campos sean correctos
    """
    start = kwargs.get("start", None)
    end = kwargs.get("end", None)
    total_tickets = kwargs.get("total_tickets", None)

    validate_start(start)
    validate_end(end)
    validate_start_end(start, end)
    validate_total_tickets(total_tickets)
    return kwargs


def get_event_by_id(id: str) -> Event:
    """
    Obtiene un evento por su id
    """
    try:
        return Event.objects.get(id=id)
    except Event.DoesNotExist:
        raise GraphQLError("No se encontró un evento con el id proporcionado")


def get_ticket_by_id(id: str) -> Ticket:
    """
    Obtiene un boleto por su id
    """
    try:
        return Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        raise GraphQLError("No se encontró un boleto con el id proporcionado")


def create_event(
    name: str,
    start: date,
    end: date,
    total_tickets: int,
) -> Event:
    """
    Crea un evento después de validar las reglas de negocio
    """
    validate_all_fields(start=start, end=end, total_tickets=total_tickets)
    event = Event(name=name, start=start, end=end, total_tickets=total_tickets)
    event.full_clean()
    event.save()
    return event


def update_event(event: Event, **kwargs) -> Event:
    """
    Actualiza un evento después de validar las reglas de negocio
    """
    validate_all_fields(**kwargs)
    total_tickets = kwargs.get("total_tickets", None)

    if total_tickets and total_tickets < event.total_sold_tickets:
        raise GraphQLError(
            "No se pueden reducir el número total de boletos por debajo de los boletos vendidos"
        )

    [setattr(event, key, value) for key, value in kwargs.items()]
    event.full_clean()
    event.save()
    return event


def delete_event(event: Event) -> Event:
    """
    Elimina un evento después de validar las reglas de negocio
    """

    if event.end >= date.today() and event.total_sold_tickets > 0:
        raise GraphQLError(
            "No se pueden eliminar eventos que aún no han terminado y tienen boletos vendidos"
        )

    event.delete()
    return event


def sell_ticket(event: Event) -> Ticket:
    """
    Crea un boleto para el evento después de validar las reglas de negocio
    """
    total_tickets = event.total_tickets

    if event.total_sold_tickets >= total_tickets:
        raise GraphQLError("No hay boletos disponibles para este evento")

    if event.end < date.today():
        raise GraphQLError(
            "No se pueden vender boletos para eventos que ya han terminado"
        )

    ticket = Ticket(event=event)
    ticket.full_clean()
    ticket.save()
    return ticket


def redeem_ticket(ticket: Ticket) -> Ticket:
    """
    Canjea un boleto después de validar las reglas de negocio
    """
    if ticket.redeemed:
        raise GraphQLError("Este boleto ya ha sido canjeado")

    if ticket.event.end < date.today():
        raise GraphQLError(
            "No se pueden canjear boletos para eventos que ya han terminado"
        )

    if ticket.event.start > date.today():
        raise GraphQLError(
            "No se pueden canjear boletos para eventos que aún no han comenzado"
        )

    ticket.redeemed = True
    ticket.full_clean()
    ticket.save()
    return ticket


def refund_ticket(ticket: Ticket) -> Ticket:
    """
    Reembolsa un boleto después de validar las reglas de negocio
    """
    if ticket.redeemed:
        raise GraphQLError("No se pueden reembolsar boletos canjeados")

    if ticket.event.end < date.today():
        raise GraphQLError(
            "No se pueden reembolsar boletos para eventos que ya han terminado"
        )

    if ticket.event.start <= date.today() and ticket.event.end > date.today():
        raise GraphQLError(
            "No se pueden reembolsar boletos para eventos que ya han comenzado"
        )

    ticket.delete()
    return ticket
