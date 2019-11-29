from django.shortcuts import render
from backend.models import *
from rest_framework import viewsets
from backend.serializers import *


# Create your views here.


# ViewSets go here (access to models through API



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmpAddressViewSet(viewsets.ModelViewSet):
    queryset = EmpAddress.objects.all()
    serializer_class = EmpAddressSerializer


class EmpNameViewSet(viewsets.ModelViewSet):
    queryset = EmpName.objects.all()
    serializer_class = EmpNameSerializer


class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class MarketMakerViewSet(viewsets.ModelViewSet):
    queryset = MarketMaker.objects.all()
    serializer_class = MarketMakerSerializer


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class ETFViewSet(viewsets.ModelViewSet):
    queryset = ETF.objects.all()
    serializer_class = ETFSerializer


class MutualFundViewSet(viewsets.ModelViewSet):
    queryset = MutualFund.objects.all()
    serializer_class = MutualFundSerializer


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class OwnsViewSet(viewsets.ModelViewSet):
    queryset = Owns.objects.all()
    serializer_class = OwnsSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class HelpViewSet(viewsets.ModelViewSet):
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class EnforceViewSet(viewsets.ModelViewSet):
    queryset = Enforce.objects.all()
    serializer_class = EnforceSerializer


class ManageViewSet(viewsets.ModelViewSet):
    queryset = Manage.objects.all()
    serializer_class = ManageSerializer
