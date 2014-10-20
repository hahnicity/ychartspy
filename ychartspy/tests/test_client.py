from mock import patch
from nose.tools import eq_, raises

from ychartspy.client import YChartsClient
from ychartspy.constants import YCHARTS_DATA_URL

RAW_DATA = [1, 2, 3]


def _make_security_params(ticker, metric):
    return [
        ("securities", "id:{},include:true".format(ticker)),
        ("calcs", "id:{},include:true".format(metric)),
        ("zoom", "1")
    ]


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
        self.client._make_request("SPY", "price", "1", "security")
        eq_(self.client.session.get.call_count, 2)
        self.client.session.get.assert_called_with(
            YCHARTS_DATA_URL, params=_make_security_params("SPY", "price")
        )

    def test_make_request_with_indicator(self):
        self.client.session.get.return_value = MockResponse()
        self.client._make_request("USRSG", "price", "1", "indicator")
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
