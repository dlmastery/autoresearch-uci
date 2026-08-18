# Autoresearch checkpoint — after Exp59 (1h still Exp30; t+6 recipe Exp59)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 59** LightGBM 31 leaves + month_sin + pres_delta + dewp_delta + **cbwd_prev_NW** · test **54.419** · val **57.601**
- vs persist-6 **61.83** skill **+12.0%**
- data: `features_horizon6.csv`
- prior side-KEEP Exp56: 54.487 / 57.658
- snapshot: `code_versions/lightgbm_t6/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 (loses to persist-1 107.80)
- **Exp56 diagnosis:** left-NW n=522 actual increment **−2.61**, Exp56 predicted **+9.11**. Staying NW calibrated.
- **Exp59:** left-NW increment **+5.69** (moved toward −2.61). Jan 83.79 · H20 63.42 · onset 92.17

## This fire
- **Exp59 DISCARD on 1h gate / side-KEEP vs Exp56.** Val 57.601 test 54.419. New t+6 recipe. Snapshotted `lightgbm_t6`.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual, Tweedie, Iws_delta, temp_delta, haze_hours6, reg_lambda=1, prev_SE/prev_cv (do not pile)

## Process
LightGBM **33/50**. Isolation holds. 1h champion unchanged. t+6 recipe moved Exp56 → Exp59. Snapshot written.

## Next pasteable
Stay on **Exp59**. Do not add other prev-direction dummies. Fill remaining LGB 17 or leave the feature set. Do not shave 1h HPs. Do not start CatBoost/MLP until LGB 50 or `lightgbm_final`.
