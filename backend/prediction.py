# from backend.logic import *
#
#
# def the_big_boi (username, account_no, start):
#     return "this is not implemented yet"
from backend.logic import *

def run():
    save_prediction(get_stock_exponential_moving_average('AAPL'), 'AAPL')
    save_prediction(get_stock_exponential_moving_average('GOOGL'), 'GOOGL')
    save_prediction(get_stock_exponential_moving_average('TSLA'), 'TSLA')
    save_prediction(get_stock_exponential_moving_average('MSFT'), 'MSFT')
    save_prediction(get_stock_exponential_moving_average('AMZN'), 'AMZN')
