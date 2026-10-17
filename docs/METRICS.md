# Metrics

## Economic Health Index

EHI is a fixed benchmark aggregate on a 0--1 scale. It is not an economic
welfare function. The implementation combines six normalized scores:

```text
EHI =
  0.20 * GDP-growth score
+ 0.15 * unemployment score
+ 0.15 * inflation score
+ 0.20 * trade-balance score
+ 0.15 * export target-completion score
+ 0.15 * import target-completion score
```

The weights sum to 1.0 and are defined in
`tradewar/evaluation/config.py`.

## Component normalization

- **GDP growth:** linearly maps growth from `-5%` to `10%` onto `[0, 1]`,
  clipping outside that range.
- **Unemployment:** `1 - clip(unemployment / 25%, 0, 1)`.
- **Inflation:** `1 - clip(abs(inflation - 2%) / 6%, 0, 1)`.
- **Trade balance:** `1 - clip(abs(trade_balance / normalized_GDP) / 0.10,
  0, 1)`. The economic unit helper normalizes GDP before forming the ratio.
- **Product target completion:** for each import or export side,
  `1 - clip(weighted_absolute_gap / weighted_target, 0, 1)`, where the gap is
  `abs(realized_volume - target_volume)`. Product weights default to 1.

The current EHI extraction uses realized product flows from the state's current
quarter. This makes under-delivery after capacity-constrained settlement
visible to the completion components. Over-delivery is also a target mismatch
under the absolute-gap score.

## Step rewards and reporting

The environment's score dictionary is computed from current country state and
is returned as the `reward` value of `Env.step`. For artifact examples, EHI is
recomputed explicitly from each final country and the final-quarter realized
flows. The demos print raw 0--1 EHI values; paper tables may apply a display
scale such as multiplying by 100.

Agreement rate and dialogue acceptance are not EHI components. They can be
tracked as protocol diagnostics, but a signed agreement can still have low
value or under-deliver after settlement.
