ychartspy
=========

Python API for calling YCharts. This is by no means an official client nor do I claim
any responsibility for breaches in the [YCharts terms of services][1].

Installation
------------

    pip install ychartspy

Usage
-----
The following is example usage of the ycharts client library

    from ychartspy.client import YChartsClient

    client = YChartsClient()
    client.get_security_prices("SPY", time_length="1")  # Get all price data on the SP500 for the past year
    client.get_indicator_prices("USHS", time_length="5")  # Get all US housing starts for the past 5 years
    client.get_security_metric("F", "pe_ratio", start_date="01/06/2013")  # Get all P/E ratios for Ford from 01/06/2013 onwards

If you want ycharts data that is limited to subscribers you will need to authenticate with 
your username/password credentials

    client.authenticate("myuser", "notarealpassword")
    client.get_security_metric("MSFT", "eps_est_0q", start_date="02/05/2014")

[1]: http://ycharts.com/about/terms
