from pathlib import Path

from tradewar.data.loader import ANONYMOUS_COUNTRY_ORDER, load_countries_from_baseline


def test_anonymous_country_configs_and_partner_references() -> None:
    baseline = Path(__file__).parents[1] / "tradewar" / "data" / "baseline"
    configs = load_countries_from_baseline(str(baseline))
    assert [country.name for country in configs] == ANONYMOUS_COUNTRY_ORDER
    allowed = set(ANONYMOUS_COUNTRY_ORDER)
    for country in configs:
        assert set(country.international_relations) <= allowed
        products = country.initial_products_export + country.initial_products_import
        for product in products:
            assert set(product.trade_partners_share) <= allowed
