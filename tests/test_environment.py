from tradewar.agents import RandomAgent
from tradewar.config import Config
from tradewar.env import Env


def run_one_quarter(seed: int):
    env = Env(
        Config(),
        max_years=1,
        start_year=2025,
        scenario_config={"trace_enabled": False, "negotiation_enabled": False},
    )
    env.reset(seed=seed)
    for country in env.countries:
        env.register_agent(country.name, RandomAgent(country.name))
    _, rewards, terminated, truncated, _ = env.step(None)
    snapshot = [
        (
            country.name,
            round(country.gdp, 10),
            round(country.inflation_rate, 10),
            round(country.unemployment_rate, 10),
            round(country.trade_balance, 10),
        )
        for country in env.countries
    ]
    return snapshot, rewards, terminated, truncated, env


def test_environment_smoke() -> None:
    snapshot, rewards, terminated, truncated, env = run_one_quarter(11)
    assert len(snapshot) == 6
    assert len(rewards) == 6
    assert all(isinstance(reward, (int, float)) for reward in rewards)
    assert not terminated
    assert not truncated
    assert env.state.trade_flows


def test_fixed_seed_is_reproducible() -> None:
    first = run_one_quarter(19)[:2]
    second = run_one_quarter(19)[:2]
    assert first == second
