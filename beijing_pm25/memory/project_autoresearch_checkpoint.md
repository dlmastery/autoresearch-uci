# Autoresearch checkpoint — after Exp28 hill-climb

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 22** XGBoost
- composite **−22.470**
- 2014 test RMSE **21.122** · 2013 val RMSE **22.470**
- vs Exp1: test 21.768 → 21.122 (−0.65) · val 23.354 → 22.470
- vs 2014 persistence 22.316: skill **+5.4%**
- recipe: depth 4, lr 0.01, subsample 0.6, n_estimators 1500, early_stop 50
- features: base UCI columns + `pm25_delta1` + `inversion_spread`

## KEEP chain
1 → 2 (depth 4) → 4 (lr 0.01) → 8 (subsample 0.6) → 14 (inversion) → 15 (delta) → 22 (inversion+delta)

## Exhausted axes
depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, gamma 1, colsample 0.5, lambda 5, alpha 1, n_estimators 4000, weather lags, raw hour, subsample {0.5,1.0}, LightGBM/CatBoost starts (including on delta features).

## Next (if continue)
t+6 on the same frozen 2014 timestamps — 1-hour nowcast HP surface is locally flat. Or LightGBM *with inversion+delta* (Exp25 used delta only).

## History
28 experiments, 7 KEEP, 21 DISCARD. See `experiment_summary.md`.
