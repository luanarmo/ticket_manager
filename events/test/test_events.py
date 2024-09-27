from .factories import EventFactory, TicketFactory
from .. import views
from freezegun import freeze_time
from events.models import Ticket


@freeze_time("2022-01-01")
def test_create_event(db, api_rf):
    event_data = {
        "name": "Test Event",
        "start": "2022-01-01",
        "end": "2022-01-02",
        "total_tickets": 1,
    }
    request = api_rf.post("/events/", event_data)
    response = views.EventViewSet.as_view({"post": "create"})(request)
    assert response.status_code == 201
    assert response.data["name"] == event_data["name"]
    assert response.data["start"] == event_data["start"]
    assert response.data["end"] == event_data["end"]
    assert response.data["total_tickets"] == event_data["total_tickets"]
    assert response.data["total_sold_tickets"] == 0
    assert response.data["total_redeemed_tickets"] == 0


@freeze_time("2022-01-04")
def test_create_event_invalid_past_start_date(db, api_rf):
    event_data = {
        "name": "Test Event",
        "start": "2022-01-03",
        "end": "2022-01-04",
        "total_tickets": 50,
    }
    request = api_rf.post("/events/", event_data)
    response = views.EventViewSet.as_view({"post": "create"})(request)
    assert response.status_code == 400
    assert response.data["start"][0] == "La fecha de inicio no puede estar en el pasado"


@freeze_time("2022-01-07")
def test_create_event_invalid_past_end_date(db, api_rf):
    event_data = {
        "name": "Test Event",
        "start": "2022-01-08",
        "end": "2022-01-06",
        "total_tickets": 50,
    }
    request = api_rf.post("/events/", event_data)
    response = views.EventViewSet.as_view({"post": "create"})(request)
    assert response.status_code == 400
    assert response.data["end"][0] == "La fecha de fin no puede estar en el pasado"


@freeze_time("2022-01-10")
def test_create_event_invalid_total_tickets(db, api_rf):
    event_data = {
        "name": "Test Event",
        "start": "2022-01-10",
        "end": "2022-01-11",
        "total_tickets": 500,
    }
    request = api_rf.post("/events/", event_data)
    response = views.EventViewSet.as_view({"post": "create"})(request)
    assert response.status_code == 400
    assert (
        response.data["total_tickets"][0]
        == "El número total de boletos no puede ser mayor a 300"
    )


@freeze_time("2022-01-15")
def test_create_event_invalid_total_tickets_zero(db, api_rf):
    event_data = {
        "name": "Test Event",
        "start": "2022-01-15",
        "end": "2022-01-16",
        "total_tickets": 0,
    }
    request = api_rf.post("/events/", event_data)
    response = views.EventViewSet.as_view({"post": "create"})(request)
    assert response.status_code == 400
    assert (
        response.data["total_tickets"][0]
        == "El número total de boletos debe ser mayor que 0"
    )


@freeze_time("2022-01-15")
def test_create_event_invalid_total_tickets_negative(db, api_rf):
    event_data = {
        "name": "Test Event",
        "start": "2022-01-15",
        "end": "2022-01-16",
        "total_tickets": -50,
    }
    request = api_rf.post("/events/", event_data)
    response = views.EventViewSet.as_view({"post": "create"})(request)
    assert response.status_code == 400
    assert (
        response.data["total_tickets"][0]
        == "El número total de boletos debe ser mayor que 0"
    )


@freeze_time("2022-01-20")
def test_create_event_invalid_start_end(db, api_rf):
    event_data = {
        "name": "Test Event",
        "start": "2022-01-23",
        "end": "2022-01-22",
        "total_tickets": 50,
    }
    request = api_rf.post("/events/", event_data)
    response = views.EventViewSet.as_view({"post": "create"})(request)
    assert response.status_code == 400
    assert (
        response.data["start"][0]
        == "La fecha de inicio no puede ser mayor que la fecha de fin"
    )


@freeze_time("2020-01-03")
def test_update_event(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2020-01-01",
        end="2020-01-02",
        total_tickets=50,
    )
    event_data = {
        "name": "Updated Event",
        "start": "2020-01-04",
        "end": "2020-01-05",
        "total_tickets": 100,
    }
    request = api_rf.put(f"/events/{event.id}/", event_data)
    response = views.EventViewSet.as_view({"put": "update"})(
        request,
        pk=event.id,
    )
    event.refresh_from_db()
    assert response.status_code == 200
    assert response.data["name"] == event_data["name"]
    assert response.data["start"] == event_data["start"]
    assert response.data["end"] == event_data["end"]
    assert response.data["total_tickets"] == event_data["total_tickets"]
    assert response.data["total_sold_tickets"] == 0
    assert response.data["total_redeemed_tickets"] == 0


@freeze_time("2020-01-03")
def test_update_event_invalid_start_date(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2020-01-01",
        end="2020-01-02",
        total_tickets=50,
    )
    event_data = {
        "name": "Updated Event",
        "start": "2019-12-31",
        "end": "2020-01-05",
        "total_tickets": 100,
    }
    request = api_rf.put(f"/events/{event.id}/", event_data)
    response = views.EventViewSet.as_view({"put": "update"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert response.data["start"][0] == "La fecha de inicio no puede estar en el pasado"


@freeze_time("2020-01-03")
def test_update_event_invalid_end_date(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2020-01-01",
        end="2020-01-02",
        total_tickets=50,
    )
    event_data = {
        "name": "Updated Event",
        "start": "2020-01-01",
        "end": "2019-12-31",
        "total_tickets": 100,
    }
    request = api_rf.put(f"/events/{event.id}/", event_data)
    response = views.EventViewSet.as_view({"put": "update"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert response.data["end"][0] == "La fecha de fin no puede estar en el pasado"


@freeze_time("2020-01-03")
def test_update_event_invalid_start_end(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2020-01-01",
        end="2020-01-02",
        total_tickets=50,
    )
    event_data = {
        "name": "Updated Event",
        "start": "2020-01-07",
        "end": "2020-01-05",
        "total_tickets": 100,
    }
    request = api_rf.put(f"/events/{event.id}/", event_data)
    response = views.EventViewSet.as_view({"put": "update"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert (
        response.data["start"][0]
        == "La fecha de inicio no puede ser mayor que la fecha de fin"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_total_tickets(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2020-01-01",
        end="2020-01-02",
        total_tickets=50,
    )
    event_data = {
        "name": "Updated Event",
        "start": "2020-01-04",
        "end": "2020-01-06",
        "total_tickets": 500,
    }
    request = api_rf.put(f"/events/{event.id}/", event_data)
    response = views.EventViewSet.as_view({"put": "update"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert (
        response.data["total_tickets"][0]
        == "El número total de boletos no puede ser mayor a 300"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_total_tickets_zero(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2020-01-01",
        end="2020-01-02",
        total_tickets=50,
    )
    event_data = {
        "name": "Updated Event",
        "start": "2020-01-04",
        "end": "2020-01-06",
        "total_tickets": 0,
    }
    request = api_rf.put(f"/events/{event.id}/", event_data)
    response = views.EventViewSet.as_view({"put": "update"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert (
        response.data["total_tickets"][0]
        == "El número total de boletos debe ser mayor que 0"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_total_tickets_minus_than_sold_tickets(db, api_rf):
    """
    Crear un evento con 50 boletos, se venden 25 boletos y se intenta actualizar el evento a 20 boletos.
    Se espera un error porque no se pueden reducir el número total de boletos por debajo de los boletos vendidos.
    """
    event = EventFactory(
        name="Test Event",
        start="2020-01-02",
        end="2020-01-03",
        total_tickets=50,
    )
    TicketFactory.create_batch(25, event=event)
    event_data = {
        "name": "Updated Event",
        "start": "2020-01-04",
        "end": "2020-01-06",
        "total_tickets": 20,
    }
    request = api_rf.put(f"/events/{event.id}/", event_data)
    response = views.EventViewSet.as_view({"put": "update"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert (
        response.data["total_tickets"]
        == "No se pueden reducir el número total de boletos por debajo de los boletos vendidos"
    )


@freeze_time("2022-01-23")
def test_delete_event_finished_zero_sold_tickets(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2022-01-20",
        end="2022-01-21",
        total_tickets=50,
    )
    request = api_rf.delete(f"/events/{event.id}/")
    response = views.EventViewSet.as_view({"delete": "destroy"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 204


@freeze_time("2022-01-23")
def test_delete_event_finished_sold_tickets(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2022-01-20",
        end="2022-01-21",
        total_tickets=50,
    )
    TicketFactory.create_batch(30, event=event)
    request = api_rf.delete(f"/events/{event.id}/")
    response = views.EventViewSet.as_view({"delete": "destroy"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 204


@freeze_time("2022-09-10")
def test_delete_event_not_finished_zero_sold_tickets(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2022-09-10",
        end="2022-09-11",
        total_tickets=50,
    )

    request = api_rf.delete(f"/events/{event.id}/")
    response = views.EventViewSet.as_view({"delete": "destroy"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 204


@freeze_time("2022-09-10")
def test_delete_event_not_finished_and_sold_tickets(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2022-09-10",
        end="2022-09-11",
        total_tickets=50,
    )
    TicketFactory.create_batch(30, event=event)

    request = api_rf.delete(f"/events/{event.id}/")
    response = views.EventViewSet.as_view({"delete": "destroy"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert (
        response.data["end"] == "No se pueden eliminar eventos que aún no han terminado"
    )
    assert (
        response.data["total_sold_tickets"]
        == "No se pueden eliminar eventos con boletos vendidos"
    )


@freeze_time("2010-06-07")
def test_sell_ticket(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-06-07",
        end="2010-06-08",
        total_tickets=50,
    )
    request = api_rf.post(f"/events/{event.id}/sell_ticket/")
    response = views.EventViewSet.as_view({"post": "sell_ticket"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 201
    assert response.data["event"] == str(event.name)
    assert response.data["redeemed"] is False
    assert Ticket.objects.filter(event=event).count() == 1


@freeze_time("2010-06-08")
def test_sell_ticket_event_finished(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-06-06",
        end="2010-06-07",
        total_tickets=50,
    )
    TicketFactory.create_batch(45, event=event)
    request = api_rf.post(f"/events/{event.id}/sell_ticket/")
    response = views.EventViewSet.as_view({"post": "sell_ticket"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert (
        response.data["end"]
        == "No se pueden vender boletos para eventos que ya han terminado"
    )


@freeze_time("2010-06-06")
def test_sell_ticket_no_tickets_available(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-06-06",
        end="2010-06-07",
        total_tickets=50,
    )
    TicketFactory.create_batch(50, event=event)
    request = api_rf.post(f"/events/{event.id}/sell_ticket/")
    response = views.EventViewSet.as_view({"post": "sell_ticket"})(
        request,
        pk=event.id,
    )
    assert response.status_code == 400
    assert (
        response.data["total_tickets"] == "No hay boletos disponibles para este evento"
    )


@freeze_time("2010-07-07")
def test_redeem_ticket(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-07",
        end="2010-07-08",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=False)
    request = api_rf.patch(f"/tickets/{ticket.id}/redeem/")
    response = views.TicketViewSet.as_view({"patch": "redeem"})(
        request,
        pk=ticket.id,
    )
    ticket.refresh_from_db()
    assert response.status_code == 200
    assert response.data["redeemed"] is True


@freeze_time("2010-07-08")
def test_redeem_ticket_event_finished(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-06",
        end="2010-07-07",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=False)
    request = api_rf.patch(f"/tickets/{ticket.id}/redeem/")
    response = views.TicketViewSet.as_view({"patch": "redeem"})(
        request,
        pk=ticket.id,
    )
    assert response.status_code == 400
    assert (
        response.data["end"]
        == "No se pueden canjear boletos para eventos que ya han terminado"
    )


@freeze_time("2010-07-06")
def test_redeem_ticket_event_not_started(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-07",
        end="2010-07-08",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=False)
    request = api_rf.patch(f"/tickets/{ticket.id}/redeem/")
    response = views.TicketViewSet.as_view({"patch": "redeem"})(
        request,
        pk=ticket.id,
    )
    assert response.status_code == 400
    assert (
        response.data["start"]
        == "No se pueden canjear boletos para eventos que aún no han comenzado"
    )


@freeze_time("2010-07-07")
def test_ticket_redeem_already(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-07",
        end="2010-07-08",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=True)
    request = api_rf.patch(f"/tickets/{ticket.id}/redeem/")
    response = views.TicketViewSet.as_view({"patch": "redeem"})(
        request,
        pk=ticket.id,
    )
    assert response.status_code == 400
    assert response.data["redeemed"] == "Este boleto ya ha sido canjeado"


@freeze_time("2010-07-08")
def test_refund_ticket(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-09",
        end="2010-07-11",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=False)
    request = api_rf.delete(f"/tickets/{ticket.id}/refund/")
    response = views.TicketViewSet.as_view({"delete": "refund"})(
        request,
        pk=ticket.id,
    )

    assert response.status_code == 204
    assert not Ticket.objects.filter(pk=ticket.id).exists()
    assert Ticket.objects.count() == 0


@freeze_time("2010-07-11")
def test_refund_ticket_event_finished(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-09",
        end="2010-07-10",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=False)
    request = api_rf.delete(f"/tickets/{ticket.id}/refund/")
    response = views.TicketViewSet.as_view({"delete": "refund"})(
        request,
        pk=ticket.id,
    )
    assert response.status_code == 400
    assert (
        response.data["end"]
        == "No se pueden reembolsar boletos para eventos que ya han terminado"
    )


@freeze_time("2010-07-09")
def test_refund_ticket_event_started(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-09",
        end="2010-07-11",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=False)
    request = api_rf.delete(f"/tickets/{ticket.id}/refund/")
    response = views.TicketViewSet.as_view({"delete": "refund"})(
        request,
        pk=ticket.id,
    )
    assert response.status_code == 400
    assert (
        response.data["start"]
        == "No se pueden reembolsar boletos para eventos que ya han comenzado"
    )


@freeze_time("2010-07-09")
def test_refund_ticket_event_already_redeemed(db, api_rf):
    event = EventFactory(
        name="Test Event",
        start="2010-07-09",
        end="2010-07-11",
        total_tickets=50,
    )
    ticket = TicketFactory(event=event, redeemed=True)
    request = api_rf.delete(f"/tickets/{ticket.id}/refund/")
    response = views.TicketViewSet.as_view({"delete": "refund"})(
        request,
        pk=ticket.id,
    )
    assert response.status_code == 400
    assert response.data["redeemed"] == "No se pueden reembolsar boletos canjeados"
