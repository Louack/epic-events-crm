"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_profiles.urls import router_users, router_managers, router_salesmen, router_supports
from crm.urls import router_clients, router_contracts, router_events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('api/users/', include(router_users.urls)),
    path('api/managers/', include(router_managers.urls)),
    path('api/salesmen/', include(router_salesmen.urls)),
    path('api/supports/', include(router_supports.urls)),
    path('api/clients/', include(router_clients.urls)),
    path('api/clients/<int:client_id>/contracts/', include(router_contracts.urls)),
    path('api/clients/<int:client_id>/contracts/<int:contract_id>/events/', include(router_events.urls)),
]

admin.site.index_title = 'Epic Events CRM'
admin.site.site_header = 'Epic Events Admin'
