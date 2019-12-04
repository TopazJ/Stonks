from backend.models import *

# TODO: Notify all users when POOL is complete
# TODO: Notify user when transaction is complete
from backend.stock_access import get_stock_price_now


def nullErrorMessage(error_message):
    print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE" + error_message)


# Buy Sell


def check_balance_for_buy_transaction(username, purchase_amount):
    query = Account.objects.filter(client=Client.objects.filter(username=username))
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
                return Transaction(market_maker=None, client=eligible_account.client, account=eligible_account,
                                   trade=stock, quantity=quantity, type=Transaction.BUY)
            else:
                nullErrorMessage("FUNDS TOO LOW - CAN PURCHASE WITH POOL")
        else:
            nullErrorMessage("FUNDS TOO LOW - CANNOT PURCHASE")
    else:
        nullErrorMessage("FATAL ERROR")


def transaction_confirmation(transaction, market_maker_username):
    if isinstance(transaction, Transaction):
        market_maker = MarketMaker.objects.filter(username=market_maker_username)
        if market_maker is not None:
            transaction.market_maker = market_maker
            transaction.save()

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
                nullErrorMessage("DATABASE DUPLICATE")
        else:
            nullErrorMessage("NOT A VALID MARKET MAKER")
    else:
        nullErrorMessage("FATAL ERROR")


def is_eligible_to_sell_stock(username, account, stock, quantity):
    if isinstance(stock, Trade):
        accounts = Account.objects.filter(client=Client.objects.filter(username=username))
        if len(accounts) > 0:
            for account in accounts:
                owns = Owns.objects.filter(client=account.client, account=account, trade=stock)
                if owns.quantity > quantity:
                    return account, owns
        else:
            nullErrorMessage("NO ACCOUNT")
    else:
        nullErrorMessage("FATAL ERROR")
    return None, None


def sell_trade_transaction_creation(username, stock, quantity):
    if isinstance(stock, Trade):
        account, owns = is_eligible_to_sell_stock(username, stock, quantity)
        if account is not None and owns is not None:
            transaction = Transaction(market_maker=None, client=account.client, account=account,
                                      trade=stock, quantity=quantity, type=Transaction.SELL)
            return transaction
    else:
        nullErrorMessage("FATAL ERROR")


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
                nullErrorMessage("FUNDS TOO LOW - CAN PURCHASE WITH POOL")
        else:
            nullErrorMessage("FUNDS TOO LOW - CANNOT PURCHASE")
    else:
        nullErrorMessage("FATAL ERROR")


def pool_confirmation(pool, market_maker_username):
    if isinstance(pool, Transaction):
        market_maker = MarketMaker.objects.filter(username=market_maker_username)
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
                nullErrorMessage("DATABASE DUPLICATE")
        else:
            nullErrorMessage("NOT A VALID MARKET MAKER")
    else:
        nullErrorMessage("FATAL ERROR")


""" check authenticatipn before every function
def login(username, password):
    client = Client.objects.get(username)
    if client is not None:
        if client.password is not password:
            nullErrorMessage("WRONG PASSWORD")
        elif client.is_banned is True:
            nullErrorMessage("YOU ARE BANNED")
        else:
            return client
    else:
        nullErrorMessage("DOES NOT EXIST")
"""


def get_user_accounts(username):
    return Account.objects.filter(client=Client.objects.get(username))


def get_user_account(username, accountID):
    return Account.objects.filter(client=Client.objects.get(username)).filter(accountID=accountID)


def create_support_ticket(username):
    client = Client.objects.get(username=username)
    support = Support.objects.all().order_by('?')[:1]
    Help(client=client, support=support).save()


def access_employee_data(employee_id):
    employee = Employee.objects.filter(employeeID=employee_id)
    if employee is None:
        return nullErrorMessage("No such Employee")
    else:
        return employee


def review_account(account_id, employee_id):
    account = Account.objects.get(accountID=account_id)
    Review(account=account, client=account.client, support=Support.objects.get(employeeID=employee_id)).save()
    return account


def enforce_rules(account_id, employee_id):
    account = Account.objects.get(accountID=account_id)
    Review(account=account, client=account.client, support=Support.objects.get(employeeID=employee_id)).save()
    return account


def solve_support_ticket(help_ticket_no):
    Help.objects.get(ticket_no=help_ticket_no).delete()


def solve_support_ticket(help_ob):
    if isinstance(help_ob, Help):
        help_ob.delete()
    else:
        nullErrorMessage("NO SUCH OBJECT")


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
                  rating=rating, risk=risk).save()
    for key, value in data_ti:
        Prediction(trade=trade, prediction=value)


def get_prediction_history(stock):
    return Prediction.objects.filter(trade=stock)
