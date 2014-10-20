AVAILABLE_SECURITY_METRICS = (
    # Current valuation
    "market_cap",
    "enterprise_value",
    "pe_ratio",
    "pe_10",
    "peg_ratio",
    "earning_yield",
    "ps_ratio",
    "price_to_book_value",
    "ev_revenues",
    "ev_ebitda",
    "ev_ebit",
    "operating_pe_ratio",
    "operating_earning_yield",
    # Dividends and shares
    "shares_outstanding",
    "dividend",
    "dividend_yield",
    "cash_dividend_payout_ratio",
    "payout_ratio",
    # Profitability
    "gross_profit_margin",
    "profit_margin",
    "ebitda_margin_ttm",
    "operating_margin_ttm",
    # Management effectiveness
    "asset_utilization",
    "days_sales_outstanding",
    "days_inventory_outstanding",
    "days_payables_outstanding",
    "receivables_turnover",
    "return_on_assets",
    "return_on_equity",
    "return_on_invested_capital",
    # Liquidity and Solvency
    "altman_z_score",
    "current_ratio",
    "debt_equity_ratio",
    "free_cash_flow",
    "kz_index",
    "tangible_common_equity_ratio",
    "times_interest_earned",
    # Employee Count Metrics
    "total_employee_number",
    "revenue_per_employee_annual",
    "ni_per_employee_annual",  # Net income per employee
    # Stock Price Performance
    "market_beta_60_month",
    "one_month_return",
    "three_month_return",
    "six_month_return",
    "ytd_return",
    "one_year_return",
    "three_year_return",
    "year_high",
    "year_low",
    # Income statement
    "revenues_ttm",
    "revenues_per_share",
    "revenues_growth",
    "eps_ttm",
    "eps_growth",
    "net_income_ttm",
    # Cash flow statement
    "cash_financing_ttm",
    "cash_investing_ttm",
    "cash_operations_ttm",
    "capex",  # Cash from expenditures
    # Balance sheet
    "cash_on_hand",
    "long_term_debt",
    "assets",
    "liabilities",
    "shareholders_equity",
    "book_value_of_equity_per_share",
    "book_value_of_tangible_equity_per_share",
    # Earnings quality
    "accruals",
    "beneish_m_score",
    # Estimates
    "sales_est_0q",  # sales estimates current quarter
    "sales_est_0y",  # sales estimates current year
    "eps_est_0q",
    "eps_est_0y",
    "forward_pe_ratio",
    "forward_pe_ratio_1y",
    "forward_ps_ratio",
    "forward_ps_ratio_1y",
    # Common Size Statements
    "net_income_cs_rev"  # Net Income (% of Quarterly Revenues)
    "net_income_annual_cs_rev",
    # Risk metrics
    "max_drawdown_all",
    "historical_daily_var_1_all",
    "historical_daily_var_5_all",
    "historical_monthly_var_5_all",  # Historical Monthly VaR 95% (All)
    "historical_monthly_var_1_all",
    # Advanced metrics
    "ca_score",
    "f_score_ttm",
    "fulmer_h_score",
    "graham_number",
    "ncavps",
    "ohlson_score",
    "quality_ratio",
    "springate_score",
    "sustainable_growth_rate",
    "tobin_q",
    "zmijewski_score",
    "momentum_fractile",
    "market_cap_fractile",
    "quality_ratio_fractile",
)
YCHARTS_DATA_URL = "http://ycharts.com/charts/fund_data/json"
YCHARTS_LOGIN_URL = "http://ycharts.com/login"
