from django.urls import path
from src.application.api.v1.views import CreateContractView, GetDailyIncomeView

urlpatterns = [
    path('contracts/create/', CreateContractView.as_view(), name='create_contract'),
    path('contract/<int:pk>/', GetDailyIncomeView.as_view(), name='get_incomes')
]
