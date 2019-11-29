from backend.models import *


def check_balance_for_transaction(username, purchase_amount):
    query = Account.objects.exist(Client.objects.filter(username=username))
    account_balance_sum = 0
    for account in query:
        balance = account.balance
        if balance > purchase_amount:
            return account, True
        account_balance_sum += balance
    if account_balance_sum > purchase_amount:
        return None, True
    return None, False

def buy_trade(stock):
    if isinstance(stock, Trade):


def access_employee_data(employee_id):
    query = Employee.objects.filter(employeeID=employee_id)
    return query
