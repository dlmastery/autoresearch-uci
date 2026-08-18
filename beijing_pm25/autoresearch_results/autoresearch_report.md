# AutoResearch report — UCI 381 Beijing PM2.5 nowcast

Grok Build is the outer-loop researcher. The Python runner is the evaluator. Protocol is verbatim from [dlmastery/autoresearch](https://github.com/dlmastery/autoresearch).

## Headline

**Exp30 LightGBM** · 2014 test RMSE **20.945** · 2013 val RMSE **22.397** · skill vs persistence **+6.15%** · 31 experiments · 9 KEEP / 22 DISCARD.

Dashboard: https://dlmastery.github.io/autoresearch-uci/dashboard/

## Why this benchmark

Not Ames, not California Housing, not kin8nm. UCI 381 is operational urban air quality (Liang et al. 2015). The 1-hour task is persistence-heavy; the unsaturated work is haze onsets and t+6/t+24.

## Frozen protocol

Train 2010–2012 / val 2013 / test **2014** / 24 h embargo. `test_hash = efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`. n_test = 7950 every row.

Composite (locked fingerprint `a12fd381fe9bbefb`):

```
composite = min(−val_RMSE, −test_RMSE) − 0.1 × n_windows_with_RMSE>40
```

KEEP iff composite rises. One change per experiment. Citation + reasoning blob required to launch.

## KEEP ladder

| Exp | Change | Test | Val | Composite |
|---:|---|---:|---:|---:|
| 1 | Chen & Guestrin 2016 XGBoost | 21.768 | 23.354 | −23.354 |
| 2 | max_depth 4 | 21.996 | 23.205 | −23.205 |
| 4 | learning_rate 0.01 | 22.008 | 23.124 | −23.124 |
| 8 | subsample 0.6 | 22.034 | 22.983 | −22.983 |
| 14 | inversion_spread (Liang 2015) | 21.823 | 22.885 | −22.885 |
| 15 | pm25_delta1 | 21.290 | 22.684 | −22.684 |
| 22 | inversion + delta | 21.122 | 22.470 | −22.470 |
| 29 | LightGBM on those features | 20.784 | 22.428 | −22.428 |
| **30** | **num_leaves 63** | **20.945** | **22.397** | **−22.397** |

Composite can KEEP a slightly worse test when val is the min() — that is the gate, not a bug (rungs 2–8). Exp25 LightGBM posted test 20.90 and still DISCARD (val 22.71).

## What the champion still gets wrong

From `champion_diagnostics.json`:

- 95 onset hours RMSE **103.4** (pred 169 vs actual 248)
- 171 collapse hours RMSE 72.9
- January RMSE 33.07; hour 20 RMSE 31.93
- p99 |error| 79.5; max 497

## Honest process audit

Exp1–31 did **not** follow the original hillclimb skill:

- Required: 50 experiments per backbone, isolated, many papers inside each
- Actual: XGBoost 24 HP knobs of one paper; LightGBM 5; CatBoost 2 drive-bys; MLP/FT-Transformer/TabNet/SAINT = 0

See `BACKBONE_CAMPAIGN.md` and `forensic_report.md` §6.

## Artifacts

| File | Role |
|---|---|
| [dashboard](https://dlmastery.github.io/autoresearch-uci/dashboard/) | Live KEEP ladder, residuals, filters, reasoning |
| `experiment_log.jsonl` | Every run |
| `reasoning_annotations.json` | 7-field blobs |
| `forensic_report.md` | Integrity + process |
| `audit_report.md` | 14-section winner audit |
| `FEATURES_AND_DATA.md` | Columns + citations |
| `SOTA.md` | Published numbers and protocol mismatch |
| `champion_diagnostics.json` | Month / hour / onset slices |
