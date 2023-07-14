from django.urls import path
from src.application.api.v1.views import (
    CreateContractView,
    GetDailyIncomeView,
    GetAllContractsView,
    ChangeLastContractPaymentStatus
)

urlpatterns = [
    path('create/', CreateContractView.as_view(), name='create_contract'),
    path(
        'check_payment/',
        ChangeLastContractPaymentStatus.as_view(),
        name='check_payment'
    ),
    path('<int:pk>/', GetDailyIncomeView.as_view(), name='get_incomes'),
    path('', GetAllContractsView.as_view(), name='all_contracts')
]
