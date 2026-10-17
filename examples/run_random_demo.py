#!/usr/bin/env python3
"""Run one deterministic year with the Random reference agent."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tradewar.agents import RandomAgent
from tradewar.config import Config
from tradewar.env import Env
from tradewar.evaluation import EconomicHealthMetrics, extract_country_ehi_data


def main() -> None:
    env = Env(
        Config(),
        max_years=1,
        start_year=2025,
        countries_num=6,
        scenario_config={"trace_enabled": False, "negotiation_max_rounds": 2},
    )
    env.reset(seed=7)
    for country in env.countries:
        env.register_agent(country.name, RandomAgent(country.name))
    done = False
    while not done:
        _, _, terminated, truncated, _ = env.step(None)
        done = terminated or truncated
    calculator = EconomicHealthMetrics()
    print("Random demo complete: 4 quarters, seed=7")
    for country in env.countries:
        metrics = calculator.calculate_country_metrics(
            extract_country_ehi_data(country, env.state)
        )
        print(f"{country.name}: EHI={calculator.calculate_ehi(metrics):.4f}")


if __name__ == "__main__":
    main()
