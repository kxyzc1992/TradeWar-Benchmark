# TradeWar: A Benchmark for Execution-Grounded Trade Negotiation with Adaptive LLM Agents

This directory is a review-stage artifact for DAI 2026. It provides the
standalone TradeWar benchmark environment, anonymous six-country
configurations, Economic Health Index (EHI) evaluation, and Random and
RuleBased non-LLM reference agents.

The artifact intentionally does **not** include TACTIC or other self-evolving
components, PromptLLM or MemoryLLM agents, LLM clients or prompt templates,
the complete experiment pipeline, research-question scripts, paper sources,
or generated results. It is a minimal environment artifact, not a claim that
the package reproduces every TACTIC number reported in the submission.

## Requirements

- Python 3.8 or newer
- Linux or macOS (other platforms are not tested)

Create an isolated environment and install the small dependency set:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Quick demo

Run either reference agent for one simulated year (four quarterly steps) with
a fixed seed:

```bash
python examples/run_random_demo.py
python examples/run_rulebased_demo.py
```

Expected output begins with a completion line such as:

```text
Random demo complete: 4 quarters, seed=7
Country_A: EHI=...
...
Country_F: EHI=...
```

EHI values are printed on a 0--1 scale. Exact values should be deterministic
for a fixed Python/dependency environment and seed.

## Tests

From this directory:

```bash
python -m pytest -q tests
```

The focused tests cover anonymous configuration loading, fixed-seed
reproducibility, an environment smoke transition, EHI calculation, and
agreement/economic-state integrity.

## Directory structure

```text
.
├── ARTIFACT_SCOPE.md
├── README.md
├── docs/
│   ├── ACTION_AND_AGREEMENT_SCHEMA.md
│   ├── ENVIRONMENT_RULES.md
│   └── METRICS.md
├── examples/
│   ├── run_random_demo.py
│   └── run_rulebased_demo.py
├── requirements.txt
├── tests/
└── tradewar/
    ├── agents/       # Random and RuleBased only
    ├── core/         # proposal normalization/application and protocol helpers
    ├── data/         # anonymous Country_A..Country_F configurations
    ├── economics/    # settlement and macroeconomic transitions
    ├── evaluation/   # EHI metrics and lightweight tracking
    ├── config.py
    ├── env.py
    └── state.py
```

## Scope and limitations

- The country configurations are synthetic benchmark roles labeled only
  `Country_A` through `Country_F`. Product names remain visible because they
  define the trade graph.
- The simulator is a controlled, stylized benchmark, not a forecasting model,
  welfare estimator, or source of policy advice.
- Negotiation is structured and agreements affect state only after proposal
  validation and signing. The included agents use deterministic code paths
  and require no API credentials.
- The demos use a short one-year horizon for review convenience. Submission
  experiments use longer protocols and additional agents that are outside
  this artifact.
- No license file is included because licensing remains to be decided by the
  authors.

See `ARTIFACT_SCOPE.md` for the inclusion boundary and `docs/` for the
implemented rules, schemas, and metrics.
