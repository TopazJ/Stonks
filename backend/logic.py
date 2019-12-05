from django.http import JsonResponse

from backend.models import *
from backend.stock_access import get_stock_price_now


def errorMessage(error_message):
    return JsonResponse({'status': 'error', 'message': error_message})


def successfulMessage(json_data):
    return JsonResponse({**{'status': 'success'}, **json_data})


# Buy Sell


def check_balance_for_buy_transaction(username, purchase_amount):
    query = Account.objects.filter(client=User.objects.filter(username=username).client)
    account_balance_sum = 0
    for account in query:
        balance = account.balance
        if balance > purchase_amount:
            return account, True
        account_balance_sum += balance
    if account_balance_sum > purchase_amount:
        return None, True
    return None, False


def buy_trade_transaction_creation(username, stock, quantity):
    """
    user places order
    server check if valid
    if valid, create a transaction object
    notify website

    Notified market maker completes transaction
    update the transaction object
    add transaction object to database and update/create owns in database
    :param username:
    :param stock:
    :param quantity:
    :return:
    """
    if isinstance(stock, Trade):
        eligible_account, can_purchase = check_balance_for_buy_transaction(username, stock.price * quantity)
        if can_purchase:
            if eligible_account is not None:
                transaction = Transaction(market_maker=None, client=eligible_account.client, account=eligible_account,
                                          trade=stock, quantity=quantity, type=Transaction.BUY).save()
                return transaction
            else:
                errorMessage("FUNDS TOO LOW - CAN PURCHASE WITH POOL")
        else:
            errorMessage("FUNDS TOO LOW - CANNOT PURCHASE")
    else:
        errorMessage("FATAL ERROR")


def transaction_confirmation(transaction, market_maker_username):
    if isinstance(transaction, Transaction):
        market_maker = User.objects.get(username=market_maker_username).market_maker
        if market_maker is not None:
            transaction.market_maker = market_maker
            transaction.update(market_maker=market_maker, complete=True)

            owns = Owns.objects.filter(client=transaction.client, account=transaction.account, trade=transaction.trade)

            if len(owns) is 1:
                if transaction.type is transaction.BUY:
                    owns.update(quantity=owns.quantity + transaction.quantity)
                elif transaction.type is transaction.SELL:
                    owns.update(quantity=owns.quantity - transaction.quantity)
            elif len(owns) is 0 and transaction.type is transaction.BUY:
                Owns(client=transaction.client, account=transaction.account, trade=transaction.trade,
                     quantity=transaction.quantity).save()
            else:
                errorMessage("DATABASE DUPLICATE")
        else:
            errorMessage("NOT A VALID MARKET MAKER")
    else:
        errorMessage("FATAL ERROR")


def is_eligible_to_sell_stock(username, account, stock, quantity):
    if isinstance(stock, Trade):
        accounts = Account.objects.filter(client=User.objects.filter(username=username).client)
        if len(accounts) > 0:
            for account in accounts:
                owns = Owns.objects.filter(client=account.client, account=account, trade=stock)
                if owns.quantity > quantity:
                    return account, owns
        else:
            errorMessage("NO ACCOUNT")
    else:
        errorMessage("FATAL ERROR")
    return None, None


def sell_trade_transaction_creation(username, stock, quantity):
    if isinstance(stock, Trade):
        account, owns = is_eligible_to_sell_stock(username, stock, quantity)
        if account is not None and owns is not None:
            transaction = Transaction(market_maker=None, client=account.client, account=account,
                                      trade=stock, quantity=quantity, type=Transaction.SELL).save()
            return transaction
    else:
        errorMessage("FATAL ERROR")


# POOL


def buy_into_pool(username, stock, quantity, fraction):
    """
    user buys into pool, if valid, returns pool object that can be then confirmed by a marketmaker later
    :param username:
    :param stock:
    :param quantity:
    :param fraction:
    :return:
    """
    if isinstance(stock, Trade):
        eligible_account, can_purchase = check_balance_for_buy_transaction(username, stock.price * quantity * fraction)
        if can_purchase:
            if eligible_account is not None:
                return Pool(market_maker=None, client=eligible_account.client, account=eligible_account,
                            trade=stock, quantity=quantity, type=Transaction.BUY, fraction=fraction)
            else:
                errorMessage("FUNDS TOO LOW - CAN PURCHASE WITH POOL")
        else:
            errorMessage("FUNDS TOO LOW - CANNOT PURCHASE")
    else:
        errorMessage("FATAL ERROR")


def pool_confirmation(pool, market_maker_username):
    if isinstance(pool, Transaction):
        market_maker = User.objects.filter(username=market_maker_username).marketMaker
        if market_maker is not None:
            pool.market_maker = market_maker
            pool.save()

            owns = Owns.objects.filter(client=pool.client, account=pool.account, trade=pool.trade)
            if len(owns) is 1:
                if pool.type is pool.BUY:
                    owns.update(quantity=owns.quantity + pool.quantity)
                elif pool.type is pool.SELL:
                    owns.update(quantity=owns.quantity - pool.quantity)
            elif len(owns) is 0 and pool.type is pool.BUY:
                Owns(client=pool.client, account=pool.account, trade=pool.trade,
                     quantity=pool.quantity).save()
            else:
                errorMessage("DATABASE DUPLICATE")
        else:
            errorMessage("NOT A VALID MARKET MAKER")
    else:
        errorMessage("FATAL ERROR")


""" check authenticatipn before every function
def login(username, password):
    client = User.objects.get(username)
    if client is not None:
        if client.password is not password:
            errorMessage("WRONG PASSWORD")
        elif client.is_banned is True:
            errorMessage("YOU ARE BANNED")
        else:
            return client
    else:
        errorMessage("DOES NOT EXIST")
"""


def get_user_accounts(username):
    return Account.objects.filter(client=User.objects.get(username).client)


def get_user_account(username, account_no):
    return Account.objects.filter(client=User.objects.get(username).client).get(account_no=account_no)


def get_transactions_by_account(username, account_no):
    return Transaction.objects.filter(account=get_user_account(username, account_no))


def create_support_ticket(username):
    client = User.objects.get(username=username).client
    support = Support.objects.all().order_by('?')[:1]
    Help(client=client, support=support).save()


def access_employee_data(employee_id):
    employee = Employee.objects.filter(employeeID=employee_id)
    if employee is None:
        return errorMessage("No such Employee")
    else:
        return employee


def review_account(account_no, employee_id, account_username):
    account = Account.objects.get(client=User.objects.get(username=account_username).client, account_no=account_no)
    Review(account=account, client=account.client, support=Support.objects.get(employeeID=employee_id)).save()
    return account


def enforce_rules(account_no, employee_id, account_username):
    account = Account.objects.get(user=User.objects.get(username=account_username), account_no=account_no)
    Review(account=account, client=account.client, support=Support.objects.get(employeeID=employee_id)).save()
    return account


def solve_support_ticket(help_ticket_no):
    Help.objects.get(ticket_no=help_ticket_no).delete()


def solve_support_ticket(help_ob):
    if isinstance(help_ob, Help):
        help_ob.delete()
    else:
        errorMessage("NO SUCH OBJECT")


def get_all_tickets_by_support(employee_id):
    return Help.objects.filter(support=Support.objects.get(employeeID=employee_id))


def save_prediction(data_ti, ticker):
    exchange = 'TSX'
    symbol = ticker
    company_name = ticker  # TODO get it with alphavantage
    price = get_stock_price_now(ticker)
    trade_type = Trade.INDIVIDUAL
    rating = 3.0
    risk = Trade.HIGH_RISK
    trade = Trade(exchange=exchange, symbol=symbol, company_name=company_name, price=price, trade_type=trade_type,
                  rating=rating, risk=risk)

    if Trade.objects.filter(exchange=exchange, symbol=symbol) is None:
        trade.save()
    else:
        Trade.objects.filter(exchange=exchange, symbol=symbol).update(price=price, trade_type=trade_type,
                                                                      rating=rating, risk=risk)

    for key, value in data_ti:
        if Prediction.objects.filter(date=key, trade=trade) is None:
            Prediction(trade=trade, prediction=value, date=key).save()


def get_prediction_history(stock):
    return Prediction.objects.filter(trade=stock)


def register_employee(username, password, employee_id, ssn, salary):
    if User.objects.get(username=username).employee is None:
        Employee(user=User(username=username, password=password), employeeID=employee_id, SSN=ssn, salary=salary).save()
        return successfulMessage({})
    else:
        return errorMessage("ID ALREADY USED")


def register_client(username, password):
    client = User.objects.get(username=username).client
    if client is None:
        user = User(username=username, password=password).save()
        Client(user=user).save()
        return successfulMessage({})
    elif client.is_banned is True:
        return errorMessage("BANNED")
    else:
        return errorMessage("DUPLICATE")


def get_owns(username, account_no):
    owns = Owns.objects.filter(client=User.objects.get(username=username).client,
                               account=Account.objects.filter(account_no=account_no))
    return owns


def create_account(username):
    client = User.objects.get(username=username).client
    if client is not None:
        accounts = Account.objects.filter(client=client)
        account_no = len(accounts)+1
        Account(client=client, account_no=account_no).save()
        return successfulMessage({})
    else:
        return errorMessage("NO SUCH CLIENT")


def add_money_to_account(username, account_no, amount):
    account = Account.objects.get(client=User.objects.get(username=username).client, account_no=account_no)
    if account is not None and amount > 0:
        account.update(balance=account.balance+amount)
        return successfulMessage({})
    else:
        return errorMessage("Invalid account or price")
