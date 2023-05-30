from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.application.api.v1.serializers import CreateContractSerizalizer
from src.application.api.v1.formulas import (
    calculate_income_btc, calculate_income_usd
)
from src.application.models import Contract


class CreateContractView(generics.CreateAPIView):
    serializer_class = CreateContractSerizalizer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            customer=request.user
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetDailyIncomeView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        contract = Contract.objects.filter(
            pk=kwargs.get('pk'), customer_id=request.user.id
        ).values(
            'hashrate', 'contract_start', 'contract_end'
        )
        hashrate = contract[0].get('hashrate')
        contract_start = contract[0].get('contract_start')
        contract_end = contract[0].get('contract_end')
        mining_period = int((contract_end - contract_start).total_seconds())
        income_btc = calculate_income_btc(
            mining_period=mining_period,
            btc_amount=hashrate
        )
        income_usd = calculate_income_usd(
            btc_amount=hashrate,
            mining_period=mining_period
        )
        return Response(
            data={
                'income_btc': income_btc,
                'income_usd': income_usd
            },
            status=status.HTTP_200_OK
        )
