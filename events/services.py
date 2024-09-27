from .models import Event, Ticket
from datetime import date
from rest_framework.exceptions import ValidationError


def create_event(
    name: str,
    start: date,
    end: date,
    total_tickets: int,
) -> Event:
    """
    Crea un evento después de validar las reglas de negocio
    """

    event = Event(name=name, start=start, end=end, total_tickets=total_tickets)
    event.full_clean()
    event.save()
    return event


def update_event(event: Event, **kwargs) -> Event:
    """
    Actualiza un evento después de validar las reglas de negocio
    """
    total_tickets = kwargs.get("total_tickets", None)

    if total_tickets and total_tickets < event.total_sold_tickets:
        raise ValidationError(
            {
                "total_tickets": "No se pueden reducir el número total de boletos por debajo de los boletos vendidos"
            }
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
        raise ValidationError(
            {
                "end": "No se pueden eliminar eventos que aún no han terminado",
                "total_sold_tickets": "No se pueden eliminar eventos con boletos vendidos",
            }
        )

    event.delete()
    return event


def sell_ticket(event: Event) -> Ticket:
    """
    Crea un boleto para el evento después de validar las reglas de negocio
    """
    total_tickets = event.total_tickets

    if event.total_sold_tickets >= total_tickets:
        raise ValidationError(
            {"total_tickets": "No hay boletos disponibles para este evento"}
        )

    if event.end < date.today():
        raise ValidationError(
            {"end": "No se pueden vender boletos para eventos que ya han terminado"}
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
        raise ValidationError({"redeemed": "Este boleto ya ha sido canjeado"})

    if ticket.event.end < date.today():
        raise ValidationError(
            {"end": "No se pueden canjear boletos para eventos que ya han terminado"}
        )

    if ticket.event.start > date.today():
        raise ValidationError(
            {
                "start": "No se pueden canjear boletos para eventos que aún no han comenzado"
            }
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
        raise ValidationError({"redeemed": "No se pueden reembolsar boletos canjeados"})

    if ticket.event.end < date.today():
        raise ValidationError(
            {"end": "No se pueden reembolsar boletos para eventos que ya han terminado"}
        )

    if ticket.event.start <= date.today() and ticket.event.end > date.today():
        raise ValidationError(
            {
                "start": "No se pueden reembolsar boletos para eventos que ya han comenzado"
            }
        )

    ticket.delete()
    return ticket
