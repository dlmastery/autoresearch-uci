# Autoresearch checkpoint — after Pages/audit pack (still Exp31)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persistence **+6.15%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6
- features: base + `pm25_delta1` + `inversion_spread`

## Residual (computed from exp30_predictions.csv)
- Onset Δ≥50: n=95 RMSE **103.35** (pred 169 vs actual 248)
- Collapse Δ≤−50: n=171 RMSE 72.90
- January RMSE 33.07 · hour 20 RMSE 31.93
- Spike F1@75 = 0.941

## Process
Exp1–31 did **not** follow the original 50-exp × isolated-backbone × many-papers skill.
XGBoost 24/50 · LightGBM 5/50 · CatBoost 2/50 · MLP/transformers 0/50.

Recovery: isolate LightGBM. Next experiment = Ke 2017 GOSS (`boosting_type=goss`). Snapshot exists at `code_versions/lightgbm_start/`.

## Pages pack (this session)
Dashboard + forensic + 14-section audit + report + FEATURES_AND_DATA + diagnostics JSON.
Skill: `.grok/skills/autoresearch-uci/SKILL.md` (also `~/.grok/skills/autoresearch-uci/`).

## Next pasteable
Stay on LightGBM. One paper change: GOSS. Do not start CatBoost/MLP until LGB cycle is isolated.
