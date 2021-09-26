from rest_framework import serializers

from .models import Client, Contract, Event


class ClientSerializerForManager(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {'sales_contact': {'required': True}}


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('sales_contact',)

    def create(self, validated_data):
        client = super().create(validated_data)
        client.sales_contact = self.context['salesman']
        client.save()
        return client


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('sales_contact', 'client')

    def create(self, validated_data):
        contract = super().create(validated_data)
        contract.sales_contact = self.context['salesman']
        contract.client = self.context['client']
        contract.save()
        return contract


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('client', 'event_status')

    def create(self, validated_data):
        event = super().create(validated_data)
        event.event_status = self.context['contract']
        event.client = self.context['client']
        event.save()
        return event
