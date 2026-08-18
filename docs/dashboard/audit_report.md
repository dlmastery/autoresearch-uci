# 14-section explainability and audit report — Exp30 LightGBM champion

*Protocol: `winner_archive.AUDIT_SECTIONS` from `generalized_ml_autoresearch`. Numbers from `champion_diagnostics.json` and `exp30_predictions.csv` on the frozen 2014 test hash.*

## 1. Executive summary

Exp30 LightGBM is the global champion after 31 experiments (9 KEEP / 22 DISCARD). On the frozen 2014 test year (n=7950, hash `efb0012c1873e5bf…`):

- Test RMSE **20.945** vs persistence 22.316 (**skill +6.15%**) vs Exp1 21.768
- Val RMSE **22.397** (the composite bottleneck)
- Composite **−22.397**
- Spike F1@75 = **0.941**; F1@150 = **0.909**
- Remaining failure: 95 onset hours (Δ≥50) at RMSE **103.4** (pred 169 vs actual 248)

This is a real but small 1-hour skill. It is **not** a claim that the original 50-experiment × many-backbone mandate is complete.

## 2. Feature importance (permutation method)

Permutation importance was not stored by the runner for Exp1–31. LightGBM gain importance is the available surrogate until a 3-seed permutation pass is logged.

Expected ranking from the KEEP lineage (not a substitute for permutation):

1. `pm25_lag1` — persistence
2. `pm25_delta1` — Exp15 KEEP, onset momentum
3. `pm25_lag2` / recent lags
4. `Iws`, `cbwd_*` — ventilation
5. `inversion_spread` — Exp14 KEEP
6. `TEMP` / `DEWP` / calendar

**Action (still open):** run permutation RMSE-increase on the frozen 2014 test set and attach `oos_feature_importance_exp30.csv` the way the QQQ dashboard does.

## 3. Top-N feature analysis

Champion feature list (40 columns): meteorology + 24 PM2.5 lags + cyclic hour + dow/weekend + `pm25_delta1` + `inversion_spread`.

KEEP-credited additions:

| Feature | First KEEP | Test delta vs previous champion |
|---|---|---|
| `inversion_spread` | Exp14 | 22.034 → 21.823 |
| `pm25_delta1` | Exp15 | 21.823 → 21.290 (then stacked in Exp22) |
| leaf-wise LGB on that set | Exp29 | 21.122 → 20.784 test (val also improved) |
| `num_leaves` 31→63 | Exp30 | test 20.784 → 20.945, val 22.428 → 22.397 (composite KEEP) |

Redundant / discarded: `is_heating`, weather lags, raw hour.

## 4. SHAP-style local explanations

Not yet computed. Onset hours are the SHAP target: when actual jumps ≥50, the model under-predicts by ~79 MAE. Local attributions on those 95 rows should be the next explainability artifact (`shap_onset_exp30.json`).

## 5. Per-fold feature drift

Single chronological fold (2013 val / 2014 test). Drift is seasonal, not a second geographic fold.

| 2014 month | n | RMSE | Mean actual |
|---:|---:|---:|---:|
| 1 | 689 | **33.07** | 116.0 |
| 2 | 597 | 25.59 | 166.7 |
| 3 | 719 | 20.38 | 112.2 |
| 4 | 669 | 27.74 | — |
| (full table in `champion_diagnostics.json`) | | | |

January is the drift / haze-season failure. Val 2013 is systematically harder than test 2014 (22.40 vs 20.94) — the composite correctly refuses to KEEP test-only wins (Exp25).

## 6. Calibration analysis

This is a point nowcast, not a probabilistic classifier. Residual bias on onsets: mean pred 169 vs mean actual 248 (−79). Collapse hours are over-predicted (195 vs 135). The model is **conservative on jumps and sticky on drops** — the persistence prior.

Spike classification at 75 µg/m³ is well calibrated in rank (F1 0.941) because lag-1 already knows the exceedance. Onset *timing* is not.

## 7. Uncertainty sanity

GBM backbones currently emit dummy aleatoric/epistemic = 0 and confidence = 0.5 (`gbm.py`). Uncertainty columns in the prediction CSVs are **not informative**. Do not use them operationally until MC-dropout / quantile / NGBoost is a paper recipe on this backbone.

## 8. Per-regime prediction distribution

| Regime | n | RMSE | Note |
|---|---:|---:|---|
| Full 2014 test | 7950 | 20.94 | headline |
| Onset Δ≥50 | 95 | 103.35 | under-predicts |
| Collapse Δ≤−50 | 171 | 72.90 | over-predicts |
| Hour 20 | 333 | 31.93 | worst hour |
| January | 689 | 33.07 | worst month |
| Spike hours >75 | 3872 | — | F1 0.941 |

## 9. Error attribution (top winners & losers)

Largest |error| on 2014 is **497 µg/m³** (p99 = 79.5). The tail is a small number of collapse/onset hours, not a uniform 21 µg/m³ noise. Operational cost is concentrated on those hours.

Recompute top-5 losers from `exp30_predictions.csv` sorted by `abs_error` before any deployment claim.

## 10. Risk audit

| Risk | Severity | Mitigation |
|---|---|---|
| Protocol-mismatch vs Guo & Lin / Brownlee | High if compared naively | SOTA.md labels splits |
| Mandate incomplete (5/50 LGB) | Process | BACKBONE_CAMPAIGN.md |
| Val harder than test | Medium | Composite uses min(val,test) |
| Dummy uncertainty | Medium | do not ship confidence |
| 1-hour task nearly saturated | Product | next useful axis is t+6 / onset |
| Single seed | Medium | 3-seed median before declaring LGB done |

## 11. Data pipeline audit

- UCI CSV cached; not re-downloaded mid-run
- Features built once; split hashed once
- Causal lags only
- Calendar split + 24 h embargo
- Every experiment n_test = 7950
- Composite fingerprint constant

**PASS** for leakage and hash lock.

## 12. Model config complete dump

See `best_config.json`. Headline:

```
backbone: lightgbm
num_leaves: 63
learning_rate: 0.01
feature_fraction: 0.8
bagging_fraction: 0.6
n_estimators: 2000
early_stopping_rounds: 50
seed: 0
features: 40 columns including pm25_delta1, inversion_spread
split: calendar_year / beijing_pm25/data
```

## 13. Known limitations & risks

- 1-hour nowcast skill is +6% vs persistence; most of R² is lag-1
- Onset RMSE 103 vs headline 21
- Original per-backbone / per-paper campaign not done
- No permutation / SHAP artifacts yet
- No multi-seed median
- No winner `inference/predict.py` freeze until archive is completed

## 14. Deployment checklist

- [x] Frozen test hash documented
- [x] Persistence baseline on the same hash
- [x] Public dashboard + journal + summary
- [x] Forensic + this 14-section audit
- [ ] Permutation importance CSV
- [ ] Onset SHAP
- [ ] 3-seed median of Exp30
- [ ] Isolated 50-exp LightGBM paper cycle finished
- [ ] t+6 protocol on the same timestamps
- [ ] Do not deploy as a health-alert model until onset RMSE is addressed
