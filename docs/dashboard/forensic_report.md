# Forensic report — AutoResearch-UCI Beijing PM2.5

*Independent checklist against the public repo. Generated 2026-08-18. State: 31 experiments, champion Exp30.*

## 1. Executive findings

| # | Finding | Status |
|---|---|---|
| 1 | Test set is the full 2014 calendar year, n = 7950 | ✅ |
| 2 | `test_hash` locked at `efb0012c1873e5bf…e0ba79fc` | ✅ |
| 3 | Zero train/val/test index overlap (calendar_split + runner guard) | ✅ |
| 4 | No `pm25[t]` in the feature row that predicts `pm25[t]` | ✅ |
| 5 | Composite fingerprint `a12fd381fe9bbefb` unchanged across all 31 rows | ✅ |
| 6 | Persistence floor computed on the same test hash (RMSE 22.316) | ✅ |
| 7 | Champion residual slices computed from `exp30_predictions.csv` | ✅ |
| 8 | Reasoning blobs exist for launched experiments (runner gate) | ⚠️ some early HP rows are thin vs 7-field floor |
| 9 | 14-section winner audit now exists (`audit_report.md`) | ✅ written this session |
| 10 | Per-backbone 50-experiment mandate **not** followed in Exp1–31 | ⚠️ see §6 |
| 11 | GBM trio interleaved instead of isolated 50-exp cycles | ⚠️ |
| 12 | Tier-1 MLP and Tier-2 transformers never started | ⚠️ |

## 2. Champion model audit (Exp 30)

| Metric | Value |
|---|---:|
| Backbone | lightgbm |
| Test RMSE | 20.9446 |
| Val RMSE | 22.3967 |
| Composite | −22.3967 |
| MAE | 11.550 |
| R² | 0.9493 |
| IC | 0.9729 |
| Skill vs 2014 persistence | **+6.15%** |
| Spike F1 @ 75 µg/m³ | 0.941 (P 0.933 / R 0.949) |
| Spike F1 @ 150 µg/m³ | 0.909 |
| p99 \|error\| | 79.5 |
| max \|error\| | 497.1 |
| n_test | 7950 |
| Recipe | num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, n_estimators 2000, early_stop 50 |
| Extra features | `pm25_delta1`, `inversion_spread` |

## 3. Residual crisis (not a pass/fail — the remaining problem)

Computed from `trade_logs/exp30_predictions.csv` joined to `data/times.csv` on the prediction `index`.

| Slice | n | RMSE | Mean pred | Mean actual |
|---|---:|---:|---:|---:|
| Full 2014 | 7950 | 20.94 | — | — |
| Onset Δ ≥ 50 µg/m³ | 95 | **103.35** | 169 | 248 |
| Collapse Δ ≤ −50 | 171 | 72.90 | 195 | 135 |
| January | 689 | **33.07** | 113 | 116 |
| August (best month) | see diagnostics | lowest | — | — |
| Hour 20 | 333 | **31.93** | — | — |

The 1-hour task is persistence-saturated. The forensic remaining error is **episode onset**, not calm hours.

## 4. Split integrity

| Check | Value |
|---|---|
| protocol_id | `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h` |
| n_train / n_val / n_test | 21725 / 7884 / 7950 |
| unused embargo | 37 |
| test time range | 2014-01-01 00:00 → 2014-12-31 23:00 |
| Every JSONL row `per_fold_test_reports[0].n` | 7950 |

**PASS** — no experiment changed the test year.

## 5. Composite lock

All 31 JSONL rows carry `composite_fingerprint = a12fd381fe9bbefb`. Formula was not rewritten after seeing results.

## 6. Process forensic (original hillclimb skill)

The original skill (`ml-autoresearch-setup` + `CLAUDE_template.md`) requires:

1. 50 experiments **per backbone**
2. Isolation (finish one, snapshot `code_versions/<bb>_start|_final/`, then next)
3. Many research publications **inside** each backbone
4. Tier 1 (linear/ridge/MLP) + Tier 2 (FT-Transformer/TabNet/…) + Tier 3 (XGB, LGB, CatBoost as three backbones)

What happened:

| Backbone | Count | Papers actually used | Isolated cycle? |
|---|---:|---|---|
| xgboost | 24 | Chen & Guestrin 2016 HP knobs + Liang 2015 inversion | No — abandoned mid-cycle |
| lightgbm | 5 | Ke et al. 2017 defaults + num_leaves | No — jumped in at Exp20/29 |
| catboost | 2 | Prokhorenkova 2018 defaults only | No — two drive-bys |
| mlp / transformers | 0 | — | Never started |

**This is a process FAIL against the original skill**, even though the 31-run ladder is a valid Karpathy keep/discard on one family.

Recovery recorded in `BACKBONE_CAMPAIGN.md`: stay on LightGBM until 50, paper recipes first (GOSS, DART, objectives, extra-trees, linear trees), then isolated CatBoost / MLP / FT-Transformer.

## 7. Artifact completeness (vs original github.io repos)

| Artifact | Original repos | This repo after this update |
|---|---|---|
| Live dashboard with filters/sort/reasoning tabs | yes | yes |
| Ceiling vs literature | yes | yes |
| Residual / per-regime charts | yes | yes |
| Forensic report | yes | yes |
| 14-section audit | yes | yes |
| Autoresearch report | yes | yes |
| FEATURES_AND_DATA | yes | yes |
| Research journal + summary | yes | yes |
| Pages INDEX with all links | yes | yes |
| Winner archive directory | yes | partial (audit + diagnostics; model pickle TBD) |
