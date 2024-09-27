from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers
from .models import Event, Ticket
from . import services
from rest_framework.decorators import action
from rest_framework import status


class EventViewSet(viewsets.GenericViewSet):

    def get_serializer_class(self):
        actions = {
            "list": serializers.ListEventSerializer,
            "retrieve": serializers.RetrieveEventSerializer,
            "create": serializers.CreateEventSerializer,
            "update": serializers.CreateEventSerializer,
            "sell_ticket": serializers.DefaultSerializer,
        }
        return actions.get(self.action, serializers.DefaultSerializer)

    def get_queryset(self):
        return Event.objects.all()

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        serializer = self.get_serializer(self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        event = services.create_event(**valid_data)
        return Response(
            data=serializers.RetrieveEventSerializer(event).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk):
        event = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        services.update_event(event, **valid_data)
        return Response(
            data=serializers.RetrieveEventSerializer(event).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk):
        event = self.get_object()
        services.delete_event(event)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="sell_ticket",
    )
    def sell_ticket(self, request, pk):
        event = self.get_object()
        ticket = services.sell_ticket(event)
        return Response(
            data=serializers.TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED,
        )


class TicketViewSet(viewsets.GenericViewSet):

    def get_queryset(self):
        return Ticket.objects.all()

    def retrieve(self, request, pk):
        serializer = serializers.TicketSerializer(self.get_object())
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="redeem",
    )
    def redeem(self, request, pk):
        ticket = self.get_object()
        ticket_updated = services.redeem_ticket(ticket)
        serializer = serializers.TicketSerializer(ticket_updated)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="refund",
    )
    def refund(self, request, pk):
        ticket = self.get_object()
        services.refund_ticket(ticket)
        return Response(status=status.HTTP_204_NO_CONTENT)
