from rest_framework import serializers
from src.application.models import Contract


class CreateContractSerizalizer(serializers.ModelSerializer):

    class Meta:
        model = Contract

        fields = [
            'id',
            'hashrate',
            'contract_start',
            'contract_end'
        ]


class GetAllContractsSerizalizer(serializers.ModelSerializer):

    class Meta:
        model = Contract

        fields = [
            'id',
            'hashrate',
            'contract_start',
            'contract_end',
            'is_paid'
        ]


class ChangeLastContractPaymentStatusSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField()
    count = serializers.FloatField()
    crypto_type = serializers.CharField(min_lenght=3, max_length=4)
    txid = serializers.CharField()
    date = serializers.DateTimeField()

    class Meta:
        model = Contract

        fields = {
            'user_id',
            'count',
            'crypto_type',
            'txid',
            'date'
        }