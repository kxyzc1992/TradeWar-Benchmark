# TradeWar: A Benchmark for Execution-Grounded Trade Negotiation with Adaptive LLM Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](DATA_LICENSE.md)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

Official repository for **TradeWar**, a multi-country simulation benchmark for
execution-grounded trade negotiation with LLM agents.

Paper: *TradeWar: A Benchmark for Execution-Grounded Trade Negotiation with
Adaptive LLM Agents*  
Authors: Xiangyu Kong, Ruirui Yang, Xia Hou  
Venue: DAI 2026

Repository: `https://github.com/kxyzc1992/TradeWar-Benchmark`

---

<p align="center">
  <img src="docs/asset/tradewar.png"
       alt="TradeWar concept illustration: delegates sign a trade deal while promises leak from a cracked crate and the EHI gauge falls."
       width="820">
</p>

## Overview

TradeWar evaluates whether natural-language trade negotiations become
**validated, executable, and economically valuable commitments** after
settlement. Unlike agreement-only negotiation benchmarks, TradeWar runs the
full pipeline:

```text
negotiation -> grounding/validation -> signing -> capacity-constrained settlement
-> delayed macroeconomic feedback -> final Economic Health Index (EHI)
```

The benchmark contains six heterogeneous country agents, quarterly transitions
over a multi-year horizon, sparse negotiation windows, bilateral tariff and
trade-share agreements, capacity and trade-graph constraints, and delayed
macroeconomic outcomes measured by EHI.

The repository also provides **TACTIC** (Trade-aware Adaptive Consolidation and
Theory-of-mind for International Commerce), an adaptive agent that updates
persistent strategy guidance from settlement outcomes **without updating base
LLM weights**, together with the PromptLLM and MemoryLLM baselines.

---

## Benchmark at a glance

| Component | Specification |
|---|---|
| Agents | 6 heterogeneous country agents |
| Horizon | 5 years = 20 quarterly transitions |
| Negotiation windows | Once every 4 quarters |
| Action types | Natural-language messages, unilateral policies, bilateral tariff/share terms |
| Agreement schema | Parties, product, direction, term type, magnitude, duration |
| Validation | Party consistency, edge existence, supported term type, graph/share feasibility |
| Settlement | Capacity-constrained allocation over a trade graph |
| Primary metric | Final Economic Health Index (EHI, reported ×100) |
| Stress scenarios | `technology_controls`, `energy_crisis` |
| Baselines | PromptLLM, MemoryLLM, TACTIC-static, full TACTIC |

EHI aggregates normalized GDP growth, unemployment, inflation, trade balance,
export-target completion, and import-target completion using fixed benchmark
weights. EHI is an evaluation aggregate for controlled agent comparison, not a
welfare estimate or policy recommendation.

---

## Requirements

- Python 3.8 or newer
- Linux or macOS (other platforms are not tested)

Create an isolated environment and install the dependency set:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

LLM-based agents (`PromptLLM`, `MemoryLLM`, `TACTIC`) additionally require
API credentials for the underlying model. The `Random` and `RuleBased`
reference agents and all environment tests run without network access or API
keys.

---

## Quick demo

Run either non-LLM reference agent for one simulated year (four quarterly
steps) with a fixed seed:

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

Full experiment entry points (LLM agents):

```bash
# Cross-play protocol
python scripts/run_cross_play.py --config configs/cross_play.yaml \
  --seeds 0 1 2 3 4 --output results/cross_play/

# Sequential adaptation protocol
python scripts/run_sequential.py --config configs/sequential.yaml \
  --episodes 20 --seeds 0 1 2 --output results/sequential/

# Stress scenarios
python scripts/run_stress.py --config configs/stress.yaml \
  --scenarios technology_controls energy_crisis --output results/stress/
```

> Script and config names must match the released code; keep them consistent.

---

## Tests

From this directory:

```bash
python -m pytest -q tests
```

The focused tests cover anonymous configuration loading, fixed-seed
reproducibility, an environment smoke transition, EHI calculation, and
agreement/economic-state integrity.

---

## Directory structure

```text
.
├── ARTIFACT_SCOPE.md
├── README.md
├── LICENSE
├── DATA_LICENSE.md
├── docs/
│   ├── ACTION_AND_AGREEMENT_SCHEMA.md
│   ├── ENVIRONMENT_RULES.md
│   ├── METRICS.md
│   └── REPRODUCTION.md
├── examples/
│   ├── run_random_demo.py
│   └── run_rulebased_demo.py
├── scripts/
│   ├── run_cross_play.py
│   ├── run_sequential.py
│   └── run_stress.py
├── configs/
│   ├── baseline.yaml
│   ├── cross_play.yaml
│   ├── sequential.yaml
│   └── stress.yaml
├── results/            # released result tables and logs
├── requirements.txt
├── tests/
└── tradewar/
    ├── agents/         # Random, RuleBased, PromptLLM, MemoryLLM, TACTIC
    ├── core/           # proposal normalization/application and protocol helpers
    ├── data/           # anonymous Country_A..Country_F configurations
    ├── economics/      # settlement and macroeconomic transitions
    ├── evaluation/     # EHI metrics and lightweight tracking
    ├── config.py
    ├── env.py
    └── state.py
```

---

## Agents and baselines

- **Random** — uniform random action selection over the supported action space.
- **RuleBased** — deterministic heuristic negotiation and signing policy.
- **PromptLLM** — zero-shot chain-of-thought prompting.
- **MemoryLLM** — CoT plus within-episode working, episodic, and semantic memory.
- **TACTIC-static** — TACTIC modules within an episode but no cross-episode
  outcome-driven updates.
- **TACTIC** — full execution-scored memory, opponent modeling, bounded planning,
  structured reflection, and cross-episode adaptation.

TACTIC updates persistent guidance and profiles while keeping base LLM weights,
prompt templates, validation rules, and environment dynamics fixed.

---

## Evaluation

The primary metric is final-quarter EHI (×100). Diagnostic metrics include:

- cumulative GDP growth;
- export-target completion;
- import-target completion;
- agreement rate (dialogue-level comparator only);
- execution validity and realized delivery diagnostics.

Agreement rate should **not** be used as an outcome metric by itself. TradeWar
separates dialogue-level agreement, executable commitment, and post-settlement
value.

See `docs/METRICS.md` for the exact EHI definition and `docs/ENVIRONMENT_RULES.md`
for the implemented transition and settlement rules.

---

## Reproduction notes

- Use the frozen configs in `configs/`; do not edit seeds or EHI weights for
  reported comparisons.
- Cross-play uses paired reversed role assignments to control for country
  asymmetry.
- Sequential runs use the same episode order and initial conditions for each
  compared method under a seed.
- Shock scenarios are deterministic and applied at Q1 of the starting year.
- All reported EHI values use the benchmark ×100 scale.
- Country configurations are synthetic benchmark roles labeled only
  `Country_A` through `Country_F`; product names remain visible because they
  define the trade graph.

See `docs/REPRODUCTION.md` and `ARTIFACT_SCOPE.md` for the full protocol and
inclusion boundary.

---

## Scope and limitations

- The simulator is a controlled, stylized benchmark, not a forecasting model,
  welfare estimator, or source of policy advice.
- Negotiation is structured, and agreements affect state only after proposal
  validation and signing.
- The `Random` and `RuleBased` demos use a short one-year horizon for
  convenience; the submission experiments use longer protocols and the LLM-based
  agents described above.
- Delayed feedback and partial observability favor memory and reflection, so
  TACTIC's advantage may not transfer to simpler bargaining domains with
  immediate feedback.

---

## Citation

If you use TradeWar or TACTIC, please cite:

```bibtex
@inproceedings{kong2026tradewar,
  title     = {TradeWar: A Benchmark for Execution-Grounded Trade Negotiation with Adaptive LLM Agents},
  author    = {Kong, Xiangyu and Yang, Ruirui and Hou, Xia},
  booktitle = {The Eighth International Conference on Distributed Artificial Intelligence (DAI '26)},
  year      = {2026},
  address   = {Hong Kong, China}
}
```

---

## License

- **Code** in this repository is released under the [MIT License](LICENSE).
- **Benchmark data and configurations** under `data/` and `configs/` are released
  under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (see
  `DATA_LICENSE.md`).
- Third-party dependencies retain their own licenses.

---

## Contact

For questions, please open an issue or contact:

- Xiangyu Kong — xykong@bistu.edu.cn
- Ruirui Yang — yangruirui@bistu.edu.cn
- Xia Hou — houxia@bistu.edu.cn
