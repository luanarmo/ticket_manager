import graphene
from graphene_django.types import DjangoObjectType

from events.models import Event, Ticket
from events import services


class TicketType(DjangoObjectType):
    class Meta:
        model = Ticket
        fields = ("id", "event", "redeemed")


class EventType(DjangoObjectType):

    total_sold_tickets = graphene.Int()
    total_redeemed_tickets = graphene.Int()
    tickets = graphene.List(TicketType)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "start",
            "end",
            "total_tickets",
            "total_sold_tickets",
            "total_redeemed_tickets",
        )

    def resolve_tickets(self, info):
        return Ticket.objects.filter(event=self)


class Query(graphene.ObjectType):
    events = graphene.List(
        EventType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    event = graphene.Field(EventType, id=graphene.UUID(required=True))
    tickets = graphene.List(TicketType)
    tickets_by_event = graphene.Field(
        TicketType,
        event_id=graphene.UUID(required=True),
    )

    def resolve_events(
        root,
        info,
        search=None,
        first=None,
        skip=None,
        **kwargs,
    ):
        qs = Event.objects.all()

        if search:
            qs = qs.filter(name__icontains=search)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_event(root, info, id):
        return services.get_event_by_id(id)

    def resolve_tickets(root, info):
        return Ticket.objects.all()

    def resolve_tickets_by_event(root, info, event_id):
        try:
            return Ticket.objects.filter(event__id=event_id)
        except Ticket.DoesNotExist:
            return None


class CreateEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        name = graphene.String(required=True)
        start = graphene.Date(required=True)
        end = graphene.Date(required=True)
        total_tickets = graphene.Int(required=True)

    def mutate(self, info, name, start, end, total_tickets):
        event = services.create_event(name, start, end, total_tickets)
        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    ok = graphene.Boolean()
    event = graphene.Field(EventType)

    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
        start = graphene.Date()
        end = graphene.Date()
        total_tickets = graphene.Int()

    def mutate(self, info, id, name, start, end, total_tickets):
        current_event = services.get_event_by_id(id)
        event = services.update_event(
            current_event,
            name=name,
            start=start,
            end=end,
            total_tickets=total_tickets,
        )
        return UpdateEvent(ok=True, event=event)


class DeleteEvent(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(required=True)

    def mutate(self, info, id):
        event = services.get_event_by_id(id)
        services.delete_event(event)
        return DeleteEvent(ok=True)


class SellTicket(graphene.Mutation):
    ok = graphene.Boolean()
    ticket = graphene.Field(TicketType)
    event = graphene.Field(EventType)

    class Arguments:
        event_id = graphene.UUID(required=True)

    def mutate(self, info, event_id):
        event = services.get_event_by_id(event_id)
        ticket = services.sell_ticket(event)
        return SellTicket(ok=True, ticket=ticket)


class RedeemTicket(graphene.Mutation):
    ok = graphene.Boolean()
    ticket = graphene.Field(TicketType)

    class Arguments:
        ticket_id = graphene.UUID(required=True)

    def mutate(self, info, ticket_id):
        ticket = services.get_ticket_by_id(ticket_id)
        services.redeem_ticket(ticket)
        return RedeemTicket(ok=True, ticket=ticket)


class RefundTicket(graphene.Mutation):
    ok = graphene.Boolean()
    ticket = graphene.Field(TicketType)

    class Arguments:
        ticket_id = graphene.UUID(required=True)

    def mutate(self, info, ticket_id):
        ticket = services.get_ticket_by_id(ticket_id)
        services.refund_ticket(ticket)
        return RefundTicket(ok=True, ticket=ticket)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
    sell_ticket = SellTicket.Field()
    redeem_ticket = RedeemTicket.Field()
    refund_ticket = RefundTicket.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
