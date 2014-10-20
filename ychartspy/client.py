import requests

from ychartspy.constants import (
    AVAILABLE_SECURITY_METRICS, YCHARTS_DATA_URL, YCHARTS_LOGIN_URL
)


class YChartsClient(object):
    def __init__(self):
        self.session = requests.session()
        # Initialize the session
        self.session.get(YCHARTS_LOGIN_URL)

    def _get_raw_data(self, response):
        return response.json()["chart_data"][0][0]["raw_data"]

    def _make_request(self, ticker, metric, time_length, ticker_type):
        params = self._set_request_params(ticker, metric, time_length, ticker_type)
        response = self.session.get(YCHARTS_DATA_URL, params=params)
        self._validate_response(response)
        return response

    def _set_request_params(self, ticker, metric, time_length, ticker_type):
        if ticker_type == "indicator":
            security_str = "type:indicator,id:I:{},include:true".format(ticker)
        else:
            security_str = "id:{},include:true".format(ticker)
        return [
            ("securities", security_str),
            ("calcs", "id:{},include:true".format(metric)),
            ("zoom", time_length)
        ]

    def _validate_response(self, response):
        if response.status_code > 302:
            raise Exception(
                "The request to {} failed with code {}. Response text \n\n {}"
                .format(response.request.url, response.status_code, response.text)
            )

    def authenticate(self, username, password):
        response = self.session.post(
            YCHARTS_LOGIN_URL,
            data={"username": username,
                  "password": password,
                  "csrfmiddlewaretoken": self.session.cookies["csrftoken"]}
        )
        self._validate_response(response)

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

    def get_security_metric(self, ticker, metric, time_length):
        """
        Get all data for a given security metric

        :param ticker: GOOG/AAPL/etc...
        :param metric: market_cap/pe_ratio/etc.. The full list is in ychartspy.constants
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        if metric not in AVAILABLE_SECURITY_METRICS:
            raise Exception("{} is not in the list of available security metrics.".format(metric))
        response = self._make_request(ticker, metric, time_length, "security")
        return self._get_raw_data(response)
