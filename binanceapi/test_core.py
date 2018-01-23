import pytest
import requests

from binanceapi.core import BinanceAPI, Kline
from binanceapi.exceptions import ParamsException, IntervalException


@pytest.fixture
def binanceapi():
    return BinanceAPI(interval='1m', limit=10, range_=5)

@pytest.fixture
def klines():
    response = [
        [1, 2, 3, 4, 12, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 16, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 10, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 20, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 19, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 19, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 11, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 19, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 14, 6, 7, 8, 9, 10, 11, 1],
        [1, 2, 3, 4, 16, 6, 7, 8, 9, 10, 11, 1]]
    return [Kline(*kline) for kline in response]

def test_caculate_sma(binanceapi, klines):
    expected = [15.4, 16.8, 15.8, 17.6, 16.4, 15.8]
    binanceapi._generate_list_of_kline_numedtuple(klines)
    for ind, elem in enumerate(binanceapi._calculate_sma()):
        assert elem == expected[ind]


# tests for exceptions

def test_invalid_url():
    binanceapi = BinanceAPI(interval='1m')
    binanceapi.base_url = 'http://seilae.co$m$'
    with pytest.raises(requests.exceptions.RequestException):
        binanceapi._resquest_api()

def test_binanceapi_without_interval():
    with pytest.raises(ParamsException):
        BinanceAPI()

def test_binanceapi_wit_invalid_interval():
    with pytest.raises(IntervalException):
        BinanceAPI(interval='2mg')
