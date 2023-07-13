from rest_framework import serializers
from src.application.models import Contract
from src.application.api.v1.formulas import calculate_contract_price


class CreateContractSerizalizer(serializers.ModelSerializer):
    contract_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Contract

        fields = [
            'id',
            'hashrate',
            'contract_start',
            'contract_end',
            'contract_price'
        ]

    def create(self, validated_data):
        contract_data = validated_data
        contract_price = calculate_contract_price(
            contract_data=contract_data
        )
        new_contract = super().create(validated_data)
        contract_data['id'] = new_contract.id
        contract_data['contract_price'] = contract_price
        print(contract_data)
        return contract_data


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
    crypto_type = serializers.CharField(min_length=3, max_length=4)
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