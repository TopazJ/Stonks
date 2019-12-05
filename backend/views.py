from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from backend.logic import *
from backend.models import *
from rest_framework import viewsets, permissions
from backend.serializers import *
import json
from django.http import JsonResponse
from backend.stock_access import *
from django.contrib.auth.decorators import permission_required

# Create your views here.



def errorMessage(error_message):
    return JsonResponse({'status': 'error', 'message': error_message})


def successfulMessage(json_data):
    JsonResponse({**{'status': 'success'}, **json_data})

@permission_required('MarketMaker')
def buy_trade(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction = buy_trade_transaction_creation(username=data['username'], stock=data['stock'],
                                                     quantity=data['quantity'])
        if transaction is not None:
            response_data = TransactionSerializer(transaction)
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")

@permission_required('MarketMaker')
def sell_trade(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction = sell_trade_transaction_creation(username=data['username'], stock=data['stock'],
                                                      quantity=data['quantity'])
        if transaction is not None:
            response_data = TransactionSerializer(transaction)
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def complete_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_confirmation(transaction=data['transaction'], market_maker_username=data['username'])


def buy_pool(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pool = buy_into_pool(
            username=data['username'], stock=data['stock'], quantity=data['quantity'], fraction=data['fraction'])
        if pool is not None:
            response_data = PoolSerializer(pool)
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def complete_pool(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pool_confirmation(pool=data['pool'], market_maker_username=data['username'])


def daily_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        successfulMessage(get_stock_json_intraday(ticker=data['ticker']))




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
