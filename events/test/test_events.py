from graphene.test import Client
from ticket_manager.schema import schema
from freezegun import freeze_time
from .factories import EventFactory, TicketFactory


def test_list_events(db):
    EventFactory.create_batch(3)
    client = Client(schema)
    query = """
    query {
        events {
            id
            name
            totalTickets
        }
    }
    """
    result = client.execute(query)
    assert "errors" not in result
    assert len(result["data"]["events"]) == 3


def test_list_pagination_events(db):
    EventFactory.create_batch(10)
    client = Client(schema)
    query = """
    query {
        events(first: 5) {
            id
            name
            totalTickets
        }
    }
    """
    result = client.execute(query)
    assert "errors" not in result
    assert len(result["data"]["events"]) == 5


def test_list_search_events(db):
    EventFactory(name="Test Event 1")
    EventFactory(name="Test Event 2")
    EventFactory(name="Another Event")
    client = Client(schema)
    query = """
    query {
        events(search: "Test") {
            id
            name
            totalTickets
        }
    }
    """
    result = client.execute(query)
    assert "errors" not in result
    assert len(result["data"]["events"]) == 2


@freeze_time("2022-01-01")
def test_event(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2022-10-26",
        end="2022-10-27",
    )
    client = Client(schema)
    query = f"""
    query {{
        event(id: "{event.id}") {{
            id
            name
            totalTickets
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["event"]["name"] == "Test Event"


@freeze_time("2022-01-01")
def test_event_not_found(db):
    client = Client(schema)
    query = """
    query {
        event(id: "702adc6c-e30d-4f77-b8b1-4173a8afc329") {
            id
            name
            totalTickets
        }
    }
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se encontró un evento con el id proporcionado"
    )


@freeze_time("2022-01-01")
def test_create_event(db):
    client = Client(schema)
    query = """
    mutation {
        createEvent(
            name: "Test Event"
            totalTickets: 100
            start: "2022-10-26"
            end: "2022-10-27"
        ) {
            event {
                id
                name
                totalTickets
            }
        }
    }
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["createEvent"]["event"]["name"] == "Test Event"


@freeze_time("2022-09-10")
def test_create_event_invalid_past_time(db):
    client = Client(schema)
    query = """
    mutation {
        createEvent(
            name: "Test Event"
            totalTickets: 100
            start: "2022-09-09"
            end: "2022-09-10"
        ) {
            event {
                id
                name
                totalTickets
            }
        }
    }
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "La fecha de inicio no puede estar en el pasado"
    )


@freeze_time("2022-01-07")
def test_create_event_invalid_past_end_date(db):
    client = Client(schema)
    query = """
    mutation {
        createEvent(
            name: "Test Event"
            totalTickets: 100
            start: "2022-01-10"
            end: "2022-01-07"
        ) {
            event {
                id
                name
                totalTickets
            }
        }
    }
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "La fecha de inicio no puede ser mayor que la fecha de fin"
    )


@freeze_time("2022-01-10")
def test_create_event_invalid_total_tickets(db):
    client = Client(schema)
    query = """
    mutation {
        createEvent(
            name: "Test Event"
            totalTickets: 301
            start: "2022-01-10"
            end: "2022-01-11"
        ) {
            event {
                id
                name
                totalTickets
            }
        }
    }
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "El número total de boletos no puede ser mayor a 300"
    )


@freeze_time("2022-01-15")
def test_create_event_invalid_total_tickets_zero(db):
    client = Client(schema)
    query = """
    mutation {
        createEvent(
            name: "Test Event"
            totalTickets: 0
            start: "2022-01-16"
            end: "2022-01-17"
        ) {
            event {
                id
                name
                totalTickets
            }
        }
    }
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "El número total de boletos debe ser mayor que 0"
    )


@freeze_time("2022-01-15")
def test_create_event_invalid_total_tickets_negative(db):
    client = Client(schema)
    query = """
    mutation {
        createEvent(
            name: "Test Event"
            totalTickets: -1
            start: "2022-01-16"
            end: "2022-01-17"
        ) {
            event {
                id
                name
                totalTickets
            }
        }
    }
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "El número total de boletos debe ser mayor que 0"
    )


@freeze_time("2022-01-20")
def test_create_event_invalid_start_end(db):
    client = Client(schema)
    query = """
    mutation {
        createEvent(
            name: "Test Event"
            totalTickets: 100
            start: "2022-01-25"
            end: "2022-01-24"
        ) {
            event {
                id
                name
                totalTickets
            }
        }
    }
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "La fecha de inicio no puede ser mayor que la fecha de fin"
    )


@freeze_time("2020-01-03")
def test_update_event(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2020-01-01",
        end="2020-01-02",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        updateEvent(
            id: "{event.id}"
            name: "Test Event Updated"
            totalTickets: 200
            start: "2020-01-05"
            end: "2020-01-06"
        ) {{
            event {{
                id
                name
                totalTickets
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["updateEvent"]["event"]["name"] == "Test Event Updated"


@freeze_time("2020-01-03")
def test_update_event_invalid_start_date(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2020-01-01",
        end="2020-01-02",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        updateEvent(
            id: "{event.id}"
            name: "Test Event Updated"
            totalTickets: 200
            start: "2019-12-31"
            end: "2020-01-06"
        ) {{
            event {{
                id
                name
                totalTickets
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "La fecha de inicio no puede estar en el pasado"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_end_date(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2020-01-01",
        end="2020-01-02",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        updateEvent(
            id: "{event.id}"
            name: "Test Event Updated"
            totalTickets: 200
            start: "2020-01-06"
            end: "2020-01-02"
        ) {{
            event {{
                id
                name
                totalTickets
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"] == "La fecha de fin no puede estar en el pasado"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_start_end(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2020-01-01",
        end="2020-01-02",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        updateEvent(
            id: "{event.id}"
            name: "Test Event Updated"
            totalTickets: 200
            start: "2020-01-06"
            end: "2020-01-05"
        ) {{
            event {{
                id
                name
                totalTickets
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "La fecha de inicio no puede ser mayor que la fecha de fin"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_total_tickets(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2020-01-01",
        end="2020-01-02",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        updateEvent(
            id: "{event.id}"
            name: "Test Event Updated"
            totalTickets: 301
            start: "2020-01-05"
            end: "2020-01-06"
        ) {{
            event {{
                id
                name
                totalTickets
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "El número total de boletos no puede ser mayor a 300"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_total_tickets_zero(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2020-01-01",
        end="2020-01-02",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        updateEvent(
            id: "{event.id}"
            name: "Test Event Updated"
            totalTickets: 0
            start: "2020-01-05"
            end: "2020-01-06"
        ) {{
            event {{
                id
                name
                totalTickets
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "El número total de boletos debe ser mayor que 0"
    )


@freeze_time("2020-01-03")
def test_update_event_invalid_total_tickets_minus_than_sold_tickets(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=50,
        start="2020-01-01",
        end="2020-01-02",
    )
    TicketFactory.create_batch(25, event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        updateEvent(
            id: "{event.id}"
            name: "Test Event Updated"
            totalTickets: 20
            start: "2020-01-05"
            end: "2020-01-06"
        ) {{
            event {{
                id
                name
                totalTickets
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se pueden reducir el número total de boletos por debajo de los boletos vendidos"
    )


@freeze_time("2022-01-23")
def test_delete_event_finished_zero_sold_tickets(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2022-01-20",
        end="2022-01-21",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        deleteEvent(id: "{event.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["deleteEvent"]["ok"] is True


@freeze_time("2022-01-23")
def test_delete_event_finished_sold_tickets(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2022-01-20",
        end="2022-01-21",
    )
    TicketFactory.create_batch(50, event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        deleteEvent(id: "{event.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["deleteEvent"]["ok"] is True


@freeze_time("2022-09-10")
def test_delete_event_not_finished_zero_sold_tickets(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2022-09-10",
        end="2022-09-11",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        deleteEvent(id: "{event.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["deleteEvent"]["ok"] is True


@freeze_time("2022-09-10")
def test_delete_event_not_finished_and_sold_tickets(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2022-09-10",
        end="2022-09-11",
    )
    TicketFactory.create_batch(50, event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        deleteEvent(id: "{event.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se pueden eliminar eventos que aún no han terminado y tienen boletos vendidos"
    )


@freeze_time("2010-06-07")
def test_sell_ticket(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-06-07",
        end="2010-06-08",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        sellTicket(eventId: "{event.id}") {{
            ok
            ticket {{
                id
                event {{
                    id
                }}
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["sellTicket"]["ok"] is True
    assert result["data"]["sellTicket"]["ticket"]["event"]["id"] == str(event.pk)


@freeze_time("2010-06-09")
def test_sell_ticket_event_finished(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-06-07",
        end="2010-06-08",
    )
    client = Client(schema)
    query = f"""
    mutation {{
        sellTicket(eventId: "{event.id}") {{
            ok
            ticket {{
                id
                event {{
                    id
                }}
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se pueden vender boletos para eventos que ya han terminado"
    )


@freeze_time("2010-06-06")
def test_sell_ticket_no_tickets_available(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-06-07",
        end="2010-06-08",
    )
    TicketFactory.create_batch(100, event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        sellTicket(eventId: "{event.id}") {{
            ok
            ticket {{
                id
                event {{
                    id
                }}
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"] == "No hay boletos disponibles para este evento"
    )


@freeze_time("2010-07-07")
def test_redeem_ticket(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-07",
        end="2010-07-08",
    )
    ticket = TicketFactory(event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        redeemTicket(ticketId: "{ticket.id}") {{
            ok
            ticket {{
                id
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["redeemTicket"]["ok"] is True
    assert result["data"]["redeemTicket"]["ticket"]["id"] == str(ticket.pk)


@freeze_time("2010-07-09")
def test_redeem_ticket_event_finished(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-07",
        end="2010-07-08",
    )
    ticket = TicketFactory(event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        redeemTicket(ticketId: "{ticket.id}") {{
            ok
            ticket {{
                id
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se pueden canjear boletos para eventos que ya han terminado"
    )


@freeze_time("2010-07-06")
def test_redeem_ticket_event_not_started(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-07",
        end="2010-07-08",
    )
    ticket = TicketFactory(event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        redeemTicket(ticketId: "{ticket.id}") {{
            ok
            ticket {{
                id
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se pueden canjear boletos para eventos que aún no han comenzado"
    )


@freeze_time("2010-07-07")
def test_ticket_redeem_already(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-07",
        end="2010-07-08",
    )
    ticket = TicketFactory(event=event, redeemed=True)
    client = Client(schema)
    query = f"""
    mutation {{
        redeemTicket(ticketId: "{ticket.id}") {{
            ok
            ticket {{
                id
            }}
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Este boleto ya ha sido canjeado"


@freeze_time("2010-07-08")
def test_refund_ticket(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-09",
        end="2010-07-10",
    )
    ticket = TicketFactory(event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        refundTicket(ticketId: "{ticket.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" not in result
    assert result["data"]["refundTicket"]["ok"] is True


@freeze_time("2010-07-11")
def test_refund_ticket_event_finished(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-09",
        end="2010-07-10",
    )
    ticket = TicketFactory(event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        refundTicket(ticketId: "{ticket.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se pueden reembolsar boletos para eventos que ya han terminado"
    )


@freeze_time("2010-07-09")
def test_refund_ticket_event_started(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-09",
        end="2010-07-10",
    )
    ticket = TicketFactory(event=event)
    client = Client(schema)
    query = f"""
    mutation {{
        refundTicket(ticketId: "{ticket.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "No se pueden reembolsar boletos para eventos que ya han comenzado"
    )


@freeze_time("2010-07-09")
def test_refund_ticket_event_already_redeemed(db):
    event = EventFactory(
        name="Test Event",
        total_tickets=100,
        start="2010-07-09",
        end="2010-07-10",
    )
    ticket = TicketFactory(event=event, redeemed=True)
    client = Client(schema)
    query = f"""
    mutation {{
        refundTicket(ticketId: "{ticket.id}") {{
            ok
        }}
    }}
    """
    result = client.execute(query)
    assert "errors" in result
    assert result["errors"][0]["message"] == "No se pueden reembolsar boletos canjeados"
