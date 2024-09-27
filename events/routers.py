from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(prefix="events", viewset=views.EventViewSet, basename="events")
router.register(
    prefix="tickets",
    viewset=views.TicketViewSet,
    basename="tickets",
)
