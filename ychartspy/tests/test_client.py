from mock import patch
from nose.tools import eq_, raises

from ychartspy.client import YChartsClient
from ychartspy.constants import YCHARTS_URL

RAW_DATA = [1, 2, 3]


def _make_security_params(ticker, metric):
    return [
        ("securities", "id:{},include:true".format(ticker)),
        ("calcs", "id:{},include:true".format(metric)),
        ("zoom", "1")
    ]


class MockResponse(object):
    def json(self):
        return {
            "chart_data": [[{
                "raw_data": RAW_DATA
            }]]
        }


class TestYChartsClient(object):
    def setup(self):
        self.client = YChartsClient()

    @patch("ychartspy.client.requests")
    def test_make_request_with_security(self, patched_requests):
        self.client._make_request("SPY", "price", "1", "security")
        patched_requests.get.assert_called_once_with(
            YCHARTS_URL, params=_make_security_params("SPY", "price")
        )

    @patch("ychartspy.client.requests")
    def test_make_request_with_indicator(self, patched_requests):
        self.client._make_request("USRSG", "price", "1", "indicator")
        patched_requests.get.assert_called_once_with(YCHARTS_URL, params=[
            ("securities", "type:indicator,id:I:USRSG,include:true"),
            ("calcs", "id:price,include:true"),
            ("zoom", "1")
        ])

    @patch("ychartspy.client.requests")
    def test_get_security_metric(self, patched_requests):
        patched_requests.get.return_value = MockResponse()
        response = self.client.get_security_metric("AAPL", "pe_ratio", "1")
        patched_requests.get.assert_called_once_with(
            YCHARTS_URL, params=_make_security_params("AAPL", "pe_ratio")
        )
        eq_(response, RAW_DATA)

    @raises(Exception)
    @patch("ychartspy.client.requests")
    def test_get_security_metric_raises_exception(self, patched_requests):
        patched_requests.get.return_value = MockResponse()
        self.client.get_security_metric("AAPL", "foo", "1")

    def test_get_raw_data(self):
        data = self.client._get_raw_data(MockResponse())
        eq_(data, RAW_DATA)
