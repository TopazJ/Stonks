from django.shortcuts import render
from django.core import serializers
from backend.logic import *
from backend.models import *
from rest_framework import viewsets
# from backend.serializers import *
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from backend.stock_access import *


# Create your views here.


def buy_trade(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction = buy_trade_transaction_creation(request.user.get_username(), symbol=data['stock'],
                                                     quantity=data['quantity'])
        if transaction is not None:
            response_data = model_to_dict(transaction)
            # response_data = serializers.serialize('json', [transaction])
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def sell_trade(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction = sell_trade_transaction_creation(request.user.get_username(), symbol=data['stock'],
                                                      quantity=data['quantity'])
        if transaction is not None:
            response_data = serializers.serialize('json', [transaction])
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def complete_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = transaction_confirmation(transaction_id=data['id'],
                                          market_maker_username=request.user.get_username())
        if result is None:
            return errorMessage('Unable to complete transaction')
        else:
            return successfulMessage({})


def buy_pool(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pool = buy_into_pool(
            username=request.user.get_username(), symbol=data['symbol'], quantity=data['quantity'],
            fraction=data['fraction'])
        if pool is not None:
            response_data = serializers.serialize('json', pool)
            return successfulMessage(response_data)
        else:
            return errorMessage("Unable to create transaction")


def complete_pool(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = pool_confirmation(date=data['date'], client=data['client'], trade=data['trade'],
                                   market_maker_username=data['username'])
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
        result = add_money_to_account(request.user.get_username(), data['account_no'], data['amount'])
        if result is None:
            return errorMessage("Unable to add money (can't make it rain :( )")
        else:
            return successfulMessage({})


def see_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return successfulMessage(None)


def owns(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        owns = get_owns(username=request.user.get_username(), account_no=data['account_no'])
        owns = serializers.serialize('json', owns)
        return successfulMessage({'data': owns})


def get_accounts(request):
    # data = json.loads(request.body)
    accounts = get_user_accounts(request.user.get_username())
    account_list = serializers.serialize('json', accounts)
    # data['username'])
    return successfulMessage({'data': account_list})


def get_predictions (request):
    data = json.loads(request.body)
    predictions = get_prediction_history(trade = data['stock'])
    predictions_list = serializers.serialize('json', predictions)
    return successfulMessage({'data': predictions_list})


def save_predict (request):
    data = json.loads(request.body)
    save_prediction(get_stock_exponential_moving_average(data['ticker']), data['ticker'])
    return successfulMessage(None)

# TODO


def create_ticket(request):
    if request.method == 'POST':
        if create_support_ticket(request.user.get_username()):
            return successfulMessage({})
    return errorMessage("FAIL")


def account_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        account = review_account(account_no=data['account_no'], employee_id=data['employee_id'],
                                 account_username=request.user.get_username())
        if account is not None:
            account = serializers.serialize('json', account)
            return successfulMessage({'data': account})
    return errorMessage("FAIL")


def rule_enforce(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if enforce_rules(admin_username=request.user.get_username(),
                         account_username=data['account_username']) is not None:
            return successfulMessage({})
    return errorMessage("FAIL")


def solve_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if solve_support_ticket(ticket_no=data['ticket_no']) is not None:
            return successfulMessage({})
    return errorMessage("FAIL")


def get_transactions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transactions = get_transactions_by_account(username=request.user.get_username(), account_no=data['account_no'])
        if transactions:
            stuff = []
            for transaction in transactions:
                trade = transaction.trade
                data = model_to_dict(transaction)
                data['trade']=model_to_dict(trade)
                stuff.append(data)
            # transactions = serializers.serialize('json', transactions)
            return successfulMessage({'data': stuff})
    return errorMessage({})


def get_mm_transactions(request):
    if request.method == 'POST':
        mm = MarketMaker.objects.get(user=User.objects.get(username=request.user.get_username()))
        transactions = Transaction.objects.filter(market_maker=mm, complete=False)
        if transactions:
            stuff = []
            for transaction in transactions:
                if transaction.complete is False:
                    trade = transaction.trade
                    data = model_to_dict(transaction)
                    data['trade'] = model_to_dict(trade)
                    stuff.append(data)
            return successfulMessage({'data': stuff})
    return errorMessage({})

