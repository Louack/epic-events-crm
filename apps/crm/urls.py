from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, ContractViewSet, EventViewSet

router_clients = DefaultRouter()
router_clients.register(r'', ClientViewSet, basename='clients')

router_contracts = DefaultRouter()
router_contracts.register(r'', ContractViewSet, basename='contracts')

router_events = DefaultRouter()
router_events.register(r'', EventViewSet, basename='events')

urlpatterns = [
    router_clients.urls,
    router_contracts.urls,
    router_events.urls
]
