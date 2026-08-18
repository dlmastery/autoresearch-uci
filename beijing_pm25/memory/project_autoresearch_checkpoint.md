# Autoresearch checkpoint — after Exp56 (1h still Exp30; t+6 recipe Exp56)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 56** LightGBM num_leaves **31** + **month_sin** + **pres_delta** + **dewp_delta** · test **54.487** · val **57.658**
- vs persist-6 **61.83** skill **+11.9%** (1h-file lag6). Causal horizon6 `pm25_lag1` persist RMSE **63.16**.
- data: `features_horizon6.csv` (includes `pres_delta`, `dewp_delta`)
- prior side-KEEP Exp55: 54.751 / 58.038 · Exp47: 55.059 / 58.138

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 (loses to persist-1 107.80)
- **Exp55 diagnosis:** late 21–23 RMSE 64.25 vs 17–20 52.26. Weekend 57.85 vs weekday 53.45. dewp_fall & not pres_rise n=1648 actual increment **−4.14**, Exp55 predicted **+3.14** (corr with pres_delta only 0.02).
- **Exp56:** that slice flipped to **−0.22**. Jan 83.81 · H20 63.49 · onset 92.34 · actual≥200 **99.57** vs persist 99.10

## This fire
- **Exp56 DISCARD on 1h gate / side-KEEP vs Exp55.** Val 57.658 test 54.487. dewp_delta is the new t+6 recipe.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual target, Tweedie, Iws_delta, temp_delta (do not pile another weather derivative)

## Process
LightGBM **30/50**. Isolation holds. 1h champion unchanged. t+6 recipe moved Exp55 → Exp56.

## Next pasteable
Stay on **Exp56**. Do not add temp_delta or Iws_delta. Snapshot `lightgbm_t6` or leave this feature set. Do not retry residual/Tweedie/lr/ff. Do not shave 1h HPs. Do not start CatBoost/MLP until LGB 50 or snapshot.
