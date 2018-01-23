"""Calculate SMA from kline/candlestick on Binance API"""
from collections import namedtuple
import logging

import requests

from binanceapi.exceptions import IntervalException, ParamsException


log = logging.getLogger()
log.setLevel(logging.DEBUG)

Kline = namedtuple('Kline', ("open_time", "open_", "high", "low", "close",
                             "volume", "close_time", "quote_asset_volume",
                             "number_of_trades", "taker_by_bav", "taker_by_qav",
                             "ignored"))


class BinanceAPI:
    def __init__(self, interval=None, limit=200, range_=12):
        self.base_url = 'https://api.binance.com/api/v1/klines?'
        self.limit = limit
        self.range = range_
        self.interval = interval

        if not self.interval:
            raise ParamsException("Interval must have used!")

        if self.interval not in self.intervals:
            raise IntervalException("Interval not in intervals list")

    @property
    def intervals(self):
        return ('1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h',
                '1d', '3d', '1w', '1M')

    def sma(self):
        response = self._resquest_api()
        self._generate_list_of_kline_numedtuple(response)
        return self._calculate_sma()

    def _resquest_api(self):
        payload = {'symbol': 'ETHBTC',
                   'interval': self.interval, 'limit': str(self.limit)}
        try:
            log.debug('calling ' + self.base_url)
            response = requests.get(self.base_url, params=payload)
        except requests.exceptions.RequestException as he:
            raise he
        else:
            return response.json()

    def _generate_list_of_kline_numedtuple(self, response):
        """return a list of Kline numedTuple to make attributes access easy"""
        log.debug('generating sma')
        self.klines = [Kline(*kline) for kline in response]

    def _calculate_sma(self):
        yield from self._generate_averages()

    def _generate_averages(self):
        start, stop, step = 0, self.range, 1
        while stop <= self.limit:
            yield self._average(self.klines[start:stop])
            start += step
            stop += step

    def _average(self, slice_):
        return sum(float(kline.close) for kline in slice_) / self.range

def klines(event, context):
    body, status_code = None, None
    try:
        interval = str(event['pathParameters']['interval'])
        binanceapi = BinanceAPI(interval=interval)
        sma = binanceapi.sma()
    except Exception as exception:
        status_code = 404
        body = exception.__str__()
    else:
        status_code = 200
        body = [item for item in sma]

    response = {
        "statusCode": status_code,
        "body": str(body)
    }

    return response

def main():
    try:
        binanceapi = BinanceAPI(interval='1m')
        sma = binanceapi.sma()
    except Exception as exception:
        print(exception.__str__())
    else:
        print(*sma)


if __name__ == '__main__':
    main()
