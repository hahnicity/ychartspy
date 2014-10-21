from mock import patch
from nose.tools import eq_, raises

from ychartspy.client import YChartsClient
from ychartspy.constants import YCHARTS_DATA_URL

RAW_DATA = [1, 2, 3]


def _make_security_params(ticker, metric, time_length="1", start_date=None, end_date=None):
    if start_date or end_date:
        time_window = [
            ("zoom", "custom"),
            ("startDate", start_date if start_date else ""),
            ("endDate", end_date if end_date else "")
        ]
    else:
        time_window = [("zoom", time_length)]
    return [
        ("securities", "id:{},include:true".format(ticker)),
        ("calcs", "id:{},include:true".format(metric)),
    ] + time_window


class MockResponse(object):
    def __init__(self, status_code=200):
        self.status_code = status_code

    def json(self):
        return {
            "chart_data": [[{
                "raw_data": RAW_DATA
            }]]
        }


class TestYChartsClient(object):
    @patch("ychartspy.client.requests")
    def setup(self, patched_requests):
        self.client = YChartsClient()
        patched_requests.session.assert_called_once_with()
        patched_requests.session().get.assert_called_once_with("http://ycharts.com/login")

    def test_make_request_with_security(self):
        self.client.session.get.return_value = MockResponse()
        self.client._make_request("SPY", "price", "1", None, None, "security")
        eq_(self.client.session.get.call_count, 2)
        self.client.session.get.assert_called_with(
            YCHARTS_DATA_URL, params=_make_security_params("SPY", "price")
        )

    def test_make_request_with_indicator(self):
        self.client.session.get.return_value = MockResponse()
        self.client._make_request("USRSG", "price", "1", None, None, "indicator")
        eq_(self.client.session.get.call_count, 2)
        self.client.session.get.assert_called_with(YCHARTS_DATA_URL, params=[
            ("securities", "type:indicator,id:I:USRSG,include:true"),
            ("calcs", "id:price,include:true"),
            ("zoom", "1")
        ])

    def test_get_security_metric(self):
        self.client.session.get.return_value = MockResponse()
        response = self.client.get_security_metric("AAPL", "pe_ratio", "1")
        eq_(self.client.session.get.call_count, 2)
        self.client.session.get.assert_called_with(
            YCHARTS_DATA_URL, params=_make_security_params("AAPL", "pe_ratio")
        )
        eq_(response, RAW_DATA)

    @raises(Exception)
    def test_get_security_metric_raises_exception(self):
        self.client.session.get.return_value = MockResponse()
        self.client.get_security_metric("AAPL", "foo", "1")

    @raises(Exception)
    def test_get_security_metric_raises_exception_for_status(self):
        self.client.session.get.return_value = MockResponse(status_code=400)
        self.client.get_security_metric("AAPL", "pe_ratio", "1")

    def test_get_raw_data(self):
        data = self.client._get_raw_data(MockResponse())
        eq_(data, RAW_DATA)

    def test_get_security_metric_with_start_date(self):
        self.client.session.get.return_value = MockResponse()
        response = self.client.get_security_metric("AAPL", "pe_ratio", start_date="01/01/2014")
        eq_(self.client.session.get.call_count, 2)
        self.client.session.get.assert_called_with(
            YCHARTS_DATA_URL,
            params=_make_security_params("AAPL", "pe_ratio", start_date="01/01/2014")
        )
        eq_(response, RAW_DATA)

    def test_get_security_metric_with_end_date(self):
        self.client.session.get.return_value = MockResponse()
        response = self.client.get_security_metric("aapl", "pe_ratio", end_date="01/01/2014")
        eq_(self.client.session.get.call_count, 2)
        self.client.session.get.assert_called_with(
            YCHARTS_DATA_URL,
            params=_make_security_params("aapl", "pe_ratio", end_date="01/01/2014")
        )
        eq_(response, RAW_DATA)

    def test_get_security_metric_with_start_and_end_date(self):
        self.client.session.get.return_value = MockResponse()
        response = self.client.get_security_metric(
            "aapl", "pe_ratio", end_date="01/01/2014", start_date="01/01/2013"
        )
        eq_(self.client.session.get.call_count, 2)
        self.client.session.get.assert_called_with(
            YCHARTS_DATA_URL,
            params=_make_security_params(
                "aapl", "pe_ratio", end_date="01/01/2014", start_date="01/01/2013"
            )
        )
        eq_(response, RAW_DATA)

    @raises(Exception)
    def test_get_security_metric_raises_exception_for_invalid_start_date(self):
        self.client.session.get.return_value = MockResponse()
        self.client.get_security_metric(
            "aapl", "pe_ratio", end_date="01/01/2014", start_date="01-01-2013"
        )

    @raises(Exception)
    def test_get_security_metric_raises_exception_for_invalid_end_date(self):
        self.client.session.get.return_value = MockResponse()
        self.client.get_security_metric(
            "aapl", "pe_ratio", end_date="2014/01/01", start_date="01/01/2013"
        )
