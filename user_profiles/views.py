from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Manager, Salesman, Support
from .serializers import UserSerializer, ManagerSerializer, SalesmanSerializer, SupportSerializer
from .permissions import IsManager


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]


class ManagerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsManager]


class SalesmanViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer
    permission_classes = [IsManager]


class SupportViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = [IsManager]