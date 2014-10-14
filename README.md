ychartspy
=========

Python API for calling YCharts. This is by no means an official client nor do I claim
any responsibility for breaches in the [YCharts terms of services][1].

Usage
-----
The following is example usage of the ycharts client library

    from ychartspy.client import YChartsClient

    client = YChartsClient()
    client.get_security_prices("SPY", "1")  # Get all price data on the SP500 for the past year
    client.get_indicator_prices("USHS", "5")  # Get all US housing starts for the past 5 years
    client.get_security_metric("F", "pe_ratio", "6m")  # Get all P/E ratios for Ford for the last 6 months

[1]: http://ycharts.com/about/terms
