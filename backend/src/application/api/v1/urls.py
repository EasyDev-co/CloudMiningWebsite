from django.urls import path
from src.application.api.v1.views import (
    CreateContractView,
    GetDailyIncomeView,
    GetAllContractsView,
    ChangeLastContractPaymentStatus,
    CalculateContractPriceView
)

urlpatterns = [
    path('create/', CreateContractView.as_view(), name='create_contract'),
    path(
        'get_price/<str:hashrate>/<str:contract_start>/<str:contract_end>/',
        CalculateContractPriceView.as_view(),
        name='get_price'
    ),
    path(
        'check_payment/',
        ChangeLastContractPaymentStatus.as_view(),
        name='check_payment'
    ),
    path('<int:pk>/', GetDailyIncomeView.as_view(), name='get_incomes'),
    path('', GetAllContractsView.as_view(), name='all_contracts')
]
