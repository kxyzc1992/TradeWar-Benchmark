# Action and Agreement Schema

Proposals are dictionaries with zero or more of the following list fields:

```json
{
  "tariff_changes": [],
  "quota_changes": [],
  "investments": [],
  "subsidies": []
}
```

`quota_adjustments` is accepted as a compatibility alias for
`quota_changes`.

## Tariff term

```json
{
  "product": "Electronics",
  "direction": "import",
  "from": "Country_C",
  "to": "Country_A",
  "target_country": "Country_C",
  "new_tariff": 0.04
}
```

- `product` must exist on the referenced bilateral edge.
- `direction` is `import` or `export`, interpreted from the proposing
  country's perspective.
- `from`, `to`, and `target_country` identify the bilateral direction.
- `new_tariff` (or input alias `new_rate`) is normalized to `[0, 1]`.
- The environment stores tariffs on the importer-side edge and synchronizes
  the active tariff policy.

## Quota/share term

```json
{
  "product": "Electronics",
  "direction": "import",
  "from": "Country_C",
  "to": "Country_A",
  "target_country": "Country_C",
  "new_share": 0.75
}
```

- `new_share` is a fraction in `[0, 1]`.
- `desired_flow` may be supplied instead; the normalizer converts it to a
  share using the import product's target demand.
- If both fields are supplied, they must agree within the implemented
  tolerance.
- Accepted share changes update both sides of the bilateral product edge.
- Other partner shares are proportionally reduced only when needed to keep
  total committed share feasible.

## Domestic policy terms

```json
{
  "investments": [{"product": "Machinery", "amount": 2.0}],
  "subsidies": [{"product": "Food", "amount": 1.0}]
}
```

These terms are valid in unilateral action application, subject to product,
budget, and implementation caps. They are disabled when signing normalization
is called with `allow_domestic_policy_terms=False`, because bilateral signing
executes tariff and share commitments rather than domestic spending promises.

## Validation and signing

Normalization resolves the source country and counterpart, checks product-edge
existence and party direction, clamps supported numeric ranges, and records
dropped/repaired-term diagnostics. Proposal structure alone is insufficient:
both session participants must return accepting signing decisions before the
normalized agreement is applied.

Malformed values, unsupported directions, counterpart mismatches, missing
products, and infeasible desired-flow/share combinations are dropped. If no
executable term remains, the conversation does not produce an economic state
change.

## Unilateral `EconomicAction`

The action object identifies the acting country, an `ActionType`, optional
target country and products, magnitude, and optional `details`. Supported
types in the included environment are tariff increase/decrease, strategic
investment, subsidy, unified action, and no action.
