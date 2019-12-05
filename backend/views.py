from django.shortcuts import render

from backend.logic import *
from backend.models import *
from rest_framework import viewsets
from backend.serializers import *
import json
from django.http import JsonResponse
from backend.stock_access import *


# Create your views here.


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
        return successfulMessage(get_stock_json_intraday(ticker=data['ticker']))


def see_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        get_user_accounts(username=data['username'])