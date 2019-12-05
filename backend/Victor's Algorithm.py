from backend.logic import *

def the_big_boi (username, account_no, start):
    user_account = get_user_account(username, account_no)
    transactions = get_transactions_by_account(user_account)
    transactions.filter()