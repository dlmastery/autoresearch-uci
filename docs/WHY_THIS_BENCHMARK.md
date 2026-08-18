# Why Beijing PM2.5 nowcast — not Ames, not kin8nm

## Rejected

| Dataset | Why not |
|---|---|
| Kaggle House Prices (Ames) | A teaching competition. 5,000+ public notebooks, stacked GBMs sit on the noise floor (~0.10 RMSLE). Improving it is leaderboard archaeology, not research. |
| California Housing | Textbook 8-feature set. Default XGBoost is already near the published ceiling. The bundled `regression_house_prices` example is a **smoke test**, not a research target. |
| kin8nm / DELVE | Simulated robot-arm kinematics. Useful in 1996–2016 UQ papers. Not a decision anyone makes. Saturated for a first Grok port. |

## Chosen

**Beijing US-Embassy hourly PM2.5, 2010–2014 (UCI 381, Liang et al.).**

- **Useful:** nowcast current PM2.5 (µg/m³) when the reference monitor is delayed and meteorology is live. Same operational setting as `environment_stats_talk` Exp07.
- **Real:** government + embassy measurements, not a generator.
- **Not saturated:** published 1-hour nowcast RMSE is still typically **15–40+ µg/m³** depending on site, year, and whether weather is used. Mean concentration is ~100 µg/m³. Spike/exceedance F1 is the metric that matters for health alerts and is far from 1.0.
- **Honest protocol:** the series is time-ordered. Random/stratified k-fold is **forbidden** (fraud_ecommerce 2026-04-24 rule: 0.27 AUC inflation). Frozen chronological holdout: last 20% time = test, preceding 15% = val, rest = train. Test indices never change.
- **Causal features:** `pm25[t]` from `pm25[t-1…t-24]` + contemporaneous meteorology (DEWP, TEMP, PRES, cbwd, Iws, Is, Ir). Weather at t is allowed for a **nowcast**; future PM2.5 is not in any feature.

Primary metric: **RMSE** (µg/m³). Composite (higher-is-better internally):

```
composite = min(-val_RMSE, -test_RMSE) - 0.1 * n_folds_with_RMSE_above_40
```

A fold/window with RMSE > 40 µg/m³ is a "negative fold" (worse than a weak operational nowcast).

## Protocol source (cloned, not re-invented)

- `C:\Users\abhir\dlmastery-github\autoresearch` — 7-step loop + `generalized_ml_autoresearch`
- `C:\Users\abhir\dlmastery-github\environment_stats_talk` — env-stats adaptation, Exp07 nowcast contract
- `C:\Users\abhir\dlmastery-github\autoresearchtabular` — citation/reasoning gates on a tabular campaign

Grok Build is the outer-loop researcher. The Python runner is the evaluator.
