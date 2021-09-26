from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ManagerViewSet, SalesmanViewSet, SupportViewSet

router_users = DefaultRouter()
router_users.register(r'', UserViewSet)

router_managers = DefaultRouter()
router_managers.register(r'', ManagerViewSet)

router_salesmen = DefaultRouter()
router_salesmen.register(r'', SalesmanViewSet)

router_supports = DefaultRouter()
router_supports.register(r'', SupportViewSet)

urlpatterns = [
    router_users.urls,
    router_managers.urls,
    router_salesmen.urls,
    router_supports.urls
    ]
