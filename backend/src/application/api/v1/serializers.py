from rest_framework import serializers, exceptions
from src.application.models import Contract
from src.application.api.v1.formulas import calculate_contract_price

from src.application.db_commands import get_cryptocurrency_price_or_404


class GetContractPriceSerizalizer(serializers.ModelSerializer):
    contract_price = serializers.FloatField(read_only=True)
    hashrate = serializers.FloatField(write_only=True)
    contract_start = serializers.DateField(write_only=True)
    contract_end = serializers.DateField(write_only=True)

    class Meta:
        model = Contract

        fields = [
            'hashrate',
            'contract_start',
            'contract_end',
            'contract_price'
        ]

    def validate(self, attrs):
        contract_data = {
            'hashrate': attrs.get('hashrate'),
            'contract_start': attrs.get('contract_start'),
            'contract_end': attrs.get('contract_end')
        }
        contract_price = calculate_contract_price(
            contract_data=contract_data
        )
        return {
            'contract_price': contract_price
        }


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

    user_id = serializers.CharField(write_only=True)
    count = serializers.FloatField(write_only=True)
    crypto_type = serializers.CharField(
        min_length=3, max_length=4, write_only=True)

    class Meta:
        model = Contract

        fields = [
            'user_id',
            'count',
            'crypto_type'
        ]

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        customer_id = attrs.get('user_id')
        count = attrs.get('count')
        crypto_type = attrs.get('crypto_type')
        contract = self.Meta.model.objects.get(customer_id=customer_id)
        contract_data = {
            'hashrate': contract.hashrate,
            'contract_start': contract.contract_start,
            'contract_end': contract.contract_end
        }
        contract_price = calculate_contract_price(contract_data)
        current_payment = get_cryptocurrency_price_or_404(
            crypto_type=crypto_type
        )
        usdt = current_payment.usdt if crypto_type != 'usdt'\
            else current_payment
        current_payment_usdt = usdt * count
        print('PAYMENT', current_payment_usdt)
        print('CONTRACT', contract_price)
        if contract_price != current_payment_usdt:
            raise exceptions.ValidationError(
                detail={'count': 'Contract and payment amounts do not match.'},
            )
        return validated_data

    def update(self, instance, validated_data):
        instance.is_paid = True
        instance.save()
        return instance
