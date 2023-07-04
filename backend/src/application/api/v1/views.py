from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from src.application.api.v1.serializers import (
    CreateContractSerizalizer,
    GetAllContractsSerizalizer
)
from src.application.api.v1.formulas import (
    calculate_income_btc, calculate_income_usd
)
from src.application.models import Contract


class APIListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 30


class CreateContractView(generics.CreateAPIView):
    """Создание нового контракта для пользователя"""
    serializer_class = CreateContractSerizalizer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        contract = Contract.objects.filter(
            customer_id=request.user.uuid
        ).first()
        if contract.is_paid is False:
            return Response(
                data={
                    'contract':  'Previous contract not paid.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
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


class GetAllContractsView(generics.ListAPIView):
    """Выводит список всех контрактов пользователя"""
    serializer_class = GetAllContractsSerizalizer
    pagination_class = APIListPagination
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = Contract._default_manager.filter(
            customer_id=self.request.user.uuid
        )
        return queryset


class GetDailyIncomeView(APIView):
    """Просмотр ежедневного дохода по контракту"""
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        contract = Contract.objects.filter(
            pk=kwargs.get('pk'), customer_id=request.user.uuid
        ).values(
            'hashrate'
        )
        hashrate = contract[0].get('hashrate')
        income_btc = calculate_income_btc(
            btc_amount=hashrate
        )
        income_usd = calculate_income_usd(
            btc_amount=hashrate
        )
        return Response(
            data={
                'income_btc': income_btc,
                'income_usd': income_usd
            },
            status=status.HTTP_200_OK
        )


class ChangeLastContractPaymentStatus(APIView):
    """
    Меняет статус оплаты
    у последнего контракта для пользователя
    """

    def post(self, request, *args, **kwargs):
        pass