from django.shortcuts import render
from django.core import serializers
from backend.logic import *
from backend.models import *
from rest_framework import viewsets
# from backend.serializers import *
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
            response_data = None #TransactionSerializer(transaction)
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def sell_trade(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction = sell_trade_transaction_creation(username=data['username'], stock=data['stock'],
                                                      quantity=data['quantity'])
        if transaction is not None:
            response_data = None #TransactionSerializer(transaction)
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def complete_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = transaction_confirmation(transaction=data['transaction'], market_maker_username=data['username'])
        if result is None:
            return errorMessage('Unable to complete transaction')
        else:
            return successfulMessage({})


def buy_pool(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pool = buy_into_pool(
            username=data['username'], stock=data['stock'], quantity=data['quantity'], fraction=data['fraction'])
        if pool is not None:
            response_data = None #PoolSerializer(pool)
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def complete_pool(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = pool_confirmation(pool=data['pool'], market_maker_username=data['username'])
        if result is None:
            return errorMessage("Unable to complete pool")
        else:
            return successfulMessage({})


def daily_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return successfulMessage(get_stock_json_intraday(ticker=data['ticker']))


def create_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = register_client(data['username'], data['password'])
        if result is None:
            return errorMessage("Unable to create account")
        else:
            return successfulMessage({})


def add_money(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = add_money_to_account(data['username'], data['account_no'], data['amount'])
        if result is None:
            return errorMessage("Unable to add money (can't make it rain :( )")
        else:
            return successfulMessage({})


def see_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return successfulMessage(None) #AccountSerializer(get_user_accounts(username=data['username'])))


def owns (request):
    data = json.loads(request.body)
    owned = get_owns(data['username'], data['account_no'])
    return successfulMessage(None) #OwnsSerializer(owned))


def get_accounts(request):
    # data = json.loads(request.body)
    accounts = get_user_accounts(request.user.get_username())
    account_list = serializers.serialize('json', accounts)
    # data['username'])
    return successfulMessage({'data': account_list})
