from rest_framework import serializers
from src.application.models import Contract


class CreateContractSerizalizer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = Contract

        fields = [
            'id',
            'customer',
            'hashrate',
            'contract_start',
            'contract_end'
        ]
