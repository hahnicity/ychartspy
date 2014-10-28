import re

import requests

from ychartspy.constants import (
    AVAILABLE_SECURITY_METRICS, YCHARTS_DATA_URL, YCHARTS_LOGIN_URL
)


def _validate_date_input(time_length, start_date, end_date):

    if not time_length and not (start_date or end_date):
        raise Exception(
            "You must enter a time length to look from data back from the current time "
            "or a start/end date to look for"
        )
    date_pattern = re.compile("(?:\d{2}\/){2}\d{4}")
    err_msg = "Your {} date must be of the form mm/dd/yyyy yours was {}"
    if start_date and not date_pattern.search(start_date):
        raise Exception(err_msg.format("start", start_date))
    if end_date and not date_pattern.search(end_date):
        raise Exception(err_msg.format("end", end_date))


class YChartsClient(object):
    def __init__(self):
        self.session = requests.session()
        # Initialize the session
        self.session.get(YCHARTS_LOGIN_URL)

    def _get_raw_data(self, response):
        return response.json()["chart_data"][0][0]["raw_data"]

    def _make_request(self, ticker, metric, time_length, start_date, end_date, ticker_type):
        params = self._set_request_params(
            ticker, metric, time_length, start_date, end_date, ticker_type
        )
        response = self.session.get(YCHARTS_DATA_URL, params=params)
        self._validate_response(response)
        return response

    def _set_request_params(self, ticker, metric, time_length, start_date, end_date, ticker_type):
        if ticker_type == "indicator":
            security_str = "type:indicator,id:I:{},include:true".format(ticker)
        else:
            security_str = "id:{},include:true".format(ticker)
        if start_date or end_date:
            time_window = [
                ("zoom", "custom"),
                ("startDate", start_date if start_date else ""),
                ("endDate", end_date if end_date else "")
            ]
        else:
            time_window = [("zoom", time_length)]
        return [
            ("securities", security_str),
            ("calcs", "id:{},include:true".format(metric)),
        ] + time_window

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

    def get_security_prices(self, ticker, time_length=None, start_date=None, end_date=None):
        """
        Get all price data for a ticker

        :param ticker: GOOG/AAPL/etc..
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        _validate_date_input(time_length, start_date, end_date)
        response = self._make_request(ticker, "price", time_length, start_date, end_date, "security")
        return self._get_raw_data(response)

    def get_indicator_prices(self, ticker, time_length=None, start_date=None, end_date=None):
        """
        Get all price data for an indicator

        :param ticker: JPIIP/USRSG/etc...
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        _validate_date_input(time_length, start_date, end_date)
        response = self._make_request(ticker, "price", time_length, start_date, end_date, "indicator")
        return self._get_raw_data(response)

    def get_security_metric(self, ticker, metric, time_length=None, start_date=None, end_date=None):
        """
        Get all data for a given security metric

        :param ticker: GOOG/AAPL/etc...
        :param metric: market_cap/pe_ratio/etc.. The full list is in ychartspy.constants
        :param time_length: 1 year (1)/3 months (3m)/etc..
        """
        if metric not in AVAILABLE_SECURITY_METRICS:
            raise Exception("{} is not in the list of available security metrics.".format(metric))
        _validate_date_input(time_length, start_date, end_date)
        response = self._make_request(
            ticker, metric, time_length, start_date, end_date, "security"
        )
        return self._get_raw_data(response)
