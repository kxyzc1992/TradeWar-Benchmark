# Artifact Scope

## Included

- Quarterly TradeWar environment and state objects
- Capacity-constrained bilateral trade settlement
- Tariff, quota/share, investment, subsidy, and no-action handling
- Invitation, pre-meeting, bargaining, signing, validation, and agreement
  application paths
- EHI component scoring and aggregate evaluation
- Six fixed anonymous configurations in the order `Country_A` through
  `Country_F`
- Random and RuleBased non-LLM reference agents
- Two one-year fixed-seed examples
- Focused tests and mechanism documentation

## Deliberately excluded

- TACTIC, self-evolving strategies, persistent experience, reflection, and
  opponent-model memory
- PromptLLM, MemoryLLM, all LLM clients, and all prompt templates
- Full experiment runners, research-question scripts, ablation pipelines, and
  large-scale evaluation orchestration
- Generated results, logs, live-state files, memory directories, and cached
  outputs
- Paper sources, author metadata, repository history, dashboards, and web
  services
- API credentials, endpoint configuration, local paths, and machine-specific
  settings

## Review interpretation

The included material supports inspection and execution of the benchmark
mechanics and the two non-LLM reference policies. It does not by itself
reproduce the submission's complete experimental protocol or all reported
TACTIC results. The short demos are smoke runs, not substitutes for the
long-horizon study.
