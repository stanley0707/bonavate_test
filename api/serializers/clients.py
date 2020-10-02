from client import models
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class ClientSerializer(serializers.ModelSerializer):

    account = AccountSerializer(many=False)

    class Meta:
        model = models.ClientAccount
        fields = [
            'id',
            'inn',
            'cash',
            'account',
        ]


class ClientSerializerSendCashForm(serializers.Serializer):
    cash = serializers.FloatField()
    clients = serializers.ListField(required=False)
