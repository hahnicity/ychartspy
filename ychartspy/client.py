import requests

from ychartspy.constants import YCHARTS_URL


class YChartsClient(object):
    def _get_raw_data(self, response):
        return response.json()["chart_data"][0][0]["raw_data"]

    def _make_request(self, ticker, data_type, time_length, ticker_type):
        params = self._set_request_params(ticker, data_type, time_length, ticker_type)
        return requests.get(YCHARTS_URL, params=params)

    def _set_request_params(self, ticker, data_type, time_length, ticker_type):
        if ticker_type == "indicator":
            security_str = "type:indicator,id:I:{},include:true".format(ticker)
        else:
            security_str = "id:{},include:true".format(ticker)
        return [
            ("securities", security_str),
            ("calcs", "id:{},include:true".format(data_type)),
            ("zoom", time_length)
        ]

    def get_security_prices(self, ticker, time_length):
        """
        Get all price data for a ticker

        :param ticker: GOOG/AAPL/etc..
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        response = self._make_request(ticker, "price", time_length, "security")
        return self._get_raw_data(response)

    def get_indicator_prices(self, ticker, time_length):
        """
        Get all price data for an indicator

        :param ticker: JPIIP/USRSG/etc...
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        response = self._make_request(ticker, "price", time_length, "indicator")
        return self._get_raw_data(response)

    def get_eps_ttm(self, ticker, time_length):
        """
        Get all EPS for a ticker

        :param ticker: GOOG/AAPL/etc..
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        response = self._make_request(ticker, "eps_ttm", time_length, "security")
        return self._get_raw_data(response)
