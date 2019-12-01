from backend.models import *


def nullErrorMessage(error_message):
    print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE" + error_message)


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


def purchase_stock_with_account(eligible_account, stock, quantity):
    if isinstance(eligible_account, Account) and isinstance(stock, Trade):
        account_owns = Owns(Account.client, Account, stock, quantity)
        account_owns.save()
    else:
        return nullErrorMessage("FATAL ERROR")


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
        eligible_account, can_purchase = check_balance_for_transaction(username, stock.price * quantity)
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
                owns.update(quantity=owns.quantity + transaction.quantity)
            elif len(owns) is 0:
                Owns(client=transaction.client, account=transaction.account, trade=transaction.trade,
                     quantity=transaction.quantity).save()
            else:
                nullErrorMessage("DATABASE DUPLICATE")
        else:
            nullErrorMessage("NOT A VALID MARKET MAKER")
    else:
        nullErrorMessage("FATAL ERROR")


def is_eligible_to_sell_stock(username, stock, quantity):
    if isinstance(stock, Trade):
        accounts = Account.objects.exist(Client.objects.filter(username=username))
        if len(accounts) > 0:
            quantity_sum = 0
            for account in accounts:
                owns = Owns.objects.filter(client=account.client, account=account, trade=stock)
                if owns.quantity > quantity:
                    owns.quantity = owns.quantity - quantity
                    owns.save()
                    break
            # TODO logic for checking multiple accounts and subtracting from them all
        else:
            nullErrorMessage("NO ACCOUNT")
    else:
        nullErrorMessage("FATAL ERROR")


def sell_trade_solo(username, stock, quantity):
    if isinstance(stock, Trade):
        if is_eligible_to_sell_stock(username, stock, quantity):
            print("re")


def access_employee_data(employee_id):
    employee = Employee.objects.filter(employeeID=employee_id)
    if employee is None:
        return nullErrorMessage("No such Employee")
    else:
        return employee
