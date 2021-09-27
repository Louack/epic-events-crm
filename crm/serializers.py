from rest_framework import serializers

from .models import Client, Contract, Event


class ClientSerializerForManager(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()
    date_updated = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id',
            'sales_contact',
            'last_name',
            'first_name',
            'email',
            'phone',
            'mobile',
            'company',
            'date_created',
            'date_updated'
        )
        extra_kwargs = {'sales_contact': {'required': True}}

    def get_date_created(self, instance):
        return instance.date_created.strftime('%Y-%m-%d, %H:%M')

    def get_date_updated(self, instance):
        return instance.date_updated.strftime('%Y-%m-%d, %H:%M')


class ClientSerializer(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()
    date_updated = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id',
            'sales_contact',
            'last_name',
            'first_name',
            'email',
            'phone',
            'mobile',
            'company',
            'date_created',
            'date_updated'
        )
        read_only_fields = ('sales_contact',)

    def get_date_created(self, instance):
        return instance.date_created.strftime('%Y-%m-%d, %H:%M')

    def get_date_updated(self, instance):
        return instance.date_updated.strftime('%Y-%m-%d, %H:%M')

    def create(self, validated_data):
        client = super().create(validated_data)
        client.sales_contact = self.context['salesman']
        client.save()
        return client


class ContractSerializer(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()
    date_updated = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = (
            'id',
            'sales_contact',
            'client',
            'status',
            'amount',
            'payment_due',
            'date_created',
            'date_updated'
        )
        read_only_fields = ('sales_contact', 'client')

    def get_date_created(self, instance):
        return instance.date_created.strftime('%Y-%m-%d, %H:%M')

    def get_date_updated(self, instance):
        return instance.date_updated.strftime('%Y-%m-%d, %H:%M')

    def create(self, validated_data):
        contract = super().create(validated_data)
        contract.sales_contact = self.context['salesman']
        contract.client = self.context['client']
        contract.save()
        return contract


class EventSerializer(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()
    date_updated = serializers.SerializerMethodField()
    event_planned_for = serializers.SerializerMethodField()

    def get_event_planned_for(self, instance):
        return instance.event_date.strftime('%Y-%m-%d, %H:%M')

    def get_date_created(self, instance):
        return instance.date_created.strftime('%Y-%m-%d, %H:%M')

    def get_date_updated(self, instance):
        return instance.date_updated.strftime('%Y-%m-%d, %H:%M')

    class Meta:
        model = Event
        fields = (
            'id',
            'support_contact',
            'event_status',
            'client',
            'attendees',
            'notes',
            'event_date',
            'event_planned_for',
            'date_created',
            'date_updated',
        )
        read_only_fields = ('client', 'event_status', 'event_planned_for')
        extra_kwargs = {
            'event_date': {'write_only': True}
        }

    def create(self, validated_data):
        event = super().create(validated_data)
        event.event_status = self.context['contract']
        event.client = self.context['client']
        event.save()
        return event
