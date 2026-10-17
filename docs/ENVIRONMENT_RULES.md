# Environment Rules

## Time and information

An episode advances one quarter per `Env.step`. The standard benchmark uses
four quarters per simulated year. Negotiation is available in the first
quarter of each year; unilateral economic actions are collected every
quarter. A country observation contains domestic macroeconomic and
product-level information plus a public snapshot. Counterpart-specific
private objectives are not exposed as a shared global state.

## Negotiation-to-execution sequence

The implemented first-quarter path is:

1. publish disclosures to a public board;
2. send and respond to bilateral invitations;
3. establish a pre-meeting agenda;
4. exchange proposals and responses;
5. request each participant's signing decision;
6. normalize and validate a mutually signed proposal;
7. apply valid tariff/share terms to the economic state.

Dialogue alone does not change tariffs or trade shares. An unsigned, rejected,
empty, or invalid proposal has no agreement-level policy effect.

## Trade graph and settlement

Products define directed exporter-to-importer edges. A partner row stores a
share, tariff, and optional base price. For importer demand `D`, a partner
share `q` requests `q * D` on an available edge. If an exporter's aggregate
requests for a product do not exceed its capacity, requests are delivered.
If they exceed capacity, the implementation allocates capacity across
requests using the settlement priority weights and requested volumes.

Realized flows, rather than conversational offers, update imports, exports,
tariff revenue, and trade balance. Trade-share changes are mirrored on the
corresponding import and export product rows. Increasing one partner's share
beyond remaining slack proportionally scales other positive shares so the
stored total remains feasible.

## Economic transition

At quarter end the environment:

- computes capacity-constrained trade flows;
- updates country trade balances;
- calculates quarterly GDP growth from the country baseline, smoothed tariff
  and net-trade effects, bounded policy support, a global-cycle term, and
  seeded noise;
- updates unemployment using the configured Okun-style response;
- updates inflation from demand and import-price pressure with inertia;
- updates exchange rates from trade-balance and interest-rate signals;
- updates inventory and fiscal state.

The coefficients are fixed benchmark parameters in `tradewar/config.py`; they
are not fitted causal estimates. Growth and other transitions are clipped
where the implementation specifies bounds for numerical stability.

## Unilateral actions

The included action model supports:

- import-tariff increase or decrease on an existing product edge;
- strategic investment in domestic product capacity;
- subsidy spending that reduces the selected product's base price;
- a unified action containing normalized tariff, quota/share, investment, and
  subsidy terms;
- no action.

Public spending first uses treasury funds and records uncovered cost as debt.
Unilateral quota increases are restricted in the normalized policy path
because additional bilateral supply requires a signed agreement.

## Reproducibility

`Env.reset(seed=...)` seeds the environment's Python and NumPy random streams.
Each registered agent receives a deterministic country-specific seed derived
from the episode seed and anonymous country label. This isolates agent random
streams while keeping repeated runs reproducible.
