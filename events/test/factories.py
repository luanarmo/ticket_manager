import factory
from factory.faker import Faker
from factory.django import DjangoModelFactory

from events.models import Event, Ticket


class EventFactory(DjangoModelFactory):

    id = Faker("uuid4")
    name = Faker("name")
    start = Faker("date")
    end = Faker("date")
    total_tickets = Faker("random_int", min=1, max=300)
    created_at = Faker("date_time")
    updated_at = Faker("date_time")

    class Meta:
        model = Event


class TicketFactory(DjangoModelFactory):

    id = Faker("uuid4")
    event = factory.SubFactory(EventFactory)
    redeemed = False
    created_at = Faker("date_time")
    updated_at = Faker("date_time")

    class Meta:
        model = Ticket
