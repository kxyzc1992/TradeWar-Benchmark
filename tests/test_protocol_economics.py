from tradewar.config import Config
from tradewar.core.action_manager import apply_proposal, normalize_proposal
from tradewar.env import Env


def _product(country, kind: str, name: str):
    products = country.products_import if kind == "import" else country.products_export
    return next(product for product in products if product.name == name)


def test_signed_term_normalization_and_economic_application() -> None:
    env = Env(
        Config(),
        max_years=1,
        start_year=2025,
        scenario_config={"trace_enabled": False, "negotiation_enabled": False},
    )
    env.reset(seed=3)
    importer = next(country for country in env.countries if country.name == "Country_A")
    exporter = next(country for country in env.countries if country.name == "Country_C")
    proposal = {
        "tariff_changes": [
            {
                "product": "Electronics",
                "direction": "import",
                "from": exporter.name,
                "to": importer.name,
                "target_country": exporter.name,
                "new_tariff": 0.04,
            }
        ],
        "quota_changes": [
            {
                "product": "Electronics",
                "direction": "import",
                "from": exporter.name,
                "to": importer.name,
                "target_country": exporter.name,
                "new_share": 0.75,
            }
        ],
    }
    normalized = normalize_proposal(
        proposal, env.state, importer.name, counterpart_country_name=exporter.name
    )
    assert len(normalized["tariff_changes"]) == 1
    assert len(normalized["quota_changes"]) == 1

    apply_proposal(proposal, env.state, importer.name)

    import_partners = _product(importer, "import", "Electronics").trade_partners_share
    export_partners = _product(exporter, "export", "Electronics").trade_partners_share
    assert import_partners[exporter.name]["tariff"] == 0.04
    assert import_partners[exporter.name]["share"] == 0.75
    assert export_partners[importer.name]["share"] == 0.75
    assert sum(row["share"] for row in import_partners.values()) <= 1.0 + 1e-9
    assert sum(row["share"] for row in export_partners.values()) <= 1.0 + 1e-9
