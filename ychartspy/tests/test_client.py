from mock import patch
from nose.tools import eq_

from ychartspy.client import YChartsClient
from ychartspy.constants import YCHARTS_URL

RAW_DATA = [1, 2, 3]


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
        patched_requests.get.assert_called_once_with(YCHARTS_URL, params=[
            ("securities", "id:SPY,include:true"),
            ("calcs", "id:price,include:true"),
            ("zoom", "1")
        ])

    @patch("ychartspy.client.requests")
    def test_make_request_with_indicator(self, patched_requests):
        self.client._make_request("USRSG", "price", "1", "indicator")
        patched_requests.get.assert_called_once_with(YCHARTS_URL, params=[
            ("securities", "type:indicator,id:I:USRSG,include:true"),
            ("calcs", "id:price,include:true"),
            ("zoom", "1")
        ])

    def test_get_raw_data(self):
        data = self.client._get_raw_data(MockResponse())
        eq_(data, RAW_DATA)
