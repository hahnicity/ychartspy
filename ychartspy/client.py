import requests

from ychartspy.constants import YCHARTS_URL


class YChartsClient(object):
    def _get_raw_data(self, response):
        return response.json()["chart_data"][0][0]["raw_data"]

    def _make_request(self, ticker, type_, time_length):
        params = self._set_request_params(ticker, type_, time_length)
        return requests.get(YCHARTS_URL, params=params)

    def _set_request_params(self, ticker, type_, time_length):
        return [
            ("securities", "id:{},include:true".format(ticker)),
            ("calcs", "id:{},include:true".format(type_)),
            ("zoom", time_length)
        ]

    def get_prices(self, ticker, time_length):
        """
        Get all price data for a ticker

        :param ticker: GOOG/AAPL/etc..
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        response = self._make_request(ticker, "price", time_length)
        return self._get_raw_data(response)

    def get_eps_ttm(self, ticker, time_length):
        """
        Get all EPS for a ticker

        :param ticker: GOOG/AAPL/etc..
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        response = self._make_request(ticker, "eps_ttm", time_length)
        return self._get_raw_data(response)
