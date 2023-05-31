from django.urls import path
from src.application.api.v1.views import (
    CreateContractView,
    GetDailyIncomeView,
    GetAllContractsView
)

urlpatterns = [
    path('contracts/create/', CreateContractView.as_view(), name='create_contract'),
    path('contracts/<int:pk>/', GetDailyIncomeView.as_view(), name='get_incomes'),
    path('contracts/', GetAllContractsView.as_view(), name='all_contracts')
]
