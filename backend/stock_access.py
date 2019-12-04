from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

API_KEY = "3PRISUZD00VD6JBK"
period = 60


def get_stock_json_intraday(ticker):
    t1 = TimeSeries(key=API_KEY, output_format='json')
    t1a, _ = t1.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    return t1a


def get_stock_json_daily(ticker):
    t1 = TimeSeries(key=API_KEY, output_format='json')
    t1a, _ = t1.get_daily(symbol=ticker, outputsize='compact')
    return t1a


def get_stock_moving_average(ticker):
    technical_indicator = TechIndicators(key=API_KEY, output_format='json')
    data_ti, metadata_ti = technical_indicator.get_sma(symbol=ticker, interval='1min', time_period=period,
                                                       series_type='close')
    return data_ti


def get_stock_exponential_moving_average(ticker):
    technical_indicator = TechIndicators(key=API_KEY, output_format='json')
    data_ti, metadata_ti = technical_indicator.get_ema(symbol=ticker, interval='1min', time_period=period,
                                                       series_type='close')
    return data_ti
