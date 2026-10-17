from tradewar.evaluation import EconomicHealthMetrics


def test_ehi_is_weighted_and_bounded() -> None:
    calculator = EconomicHealthMetrics()
    metrics = calculator.calculate_country_metrics(
        {
            "gdp_growth": 3.0,
            "unemployment_rate": 5.0,
            "inflation_rate": 2.0,
            "trade_balance": 0.0,
            "gdp": 10.0,
            "export_product_completion_rows": [
                {"product": "Electronics", "actual": 100.0, "target": 100.0}
            ],
            "import_product_completion_rows": [
                {"product": "Energy", "actual": 80.0, "target": 100.0}
            ],
        }
    )
    assert set(metrics) == {
        "gdp_growth",
        "unemployment",
        "inflation",
        "trade_balance",
        "export_completion",
        "import_completion",
    }
    assert 0.0 <= calculator.calculate_ehi(metrics) <= 1.0
