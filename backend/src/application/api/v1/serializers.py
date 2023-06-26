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
