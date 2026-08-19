# Autoresearch checkpoint — after Exp78 (1h still Exp30; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**
- vs persist-6 **61.83** skill **+12.2%**
- lineage: Exp72 → Exp75 rh_magnus (val 57.191) → Exp76 linear_lambda=1
- snapshot: `code_versions/lightgbm_t6/` and `code_versions/lightgbm_final/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · pred +0.2 vs need +87.4
- **NEW Exp30:** hour-20 January n=29 RMSE **27.61** vs persist **25.29** (skill **−9.2%**). persist>=150 typical n=1490 RMSE **23.14** vs persist **19.34** (skill **−19.6%**), pred **−4.7**.
- **Exp77 Ordered:** h20 Jan **31.30** (worse); onset pred **−3.3**.
- **Exp78 Plain NEAR-MISS:** h20 Jan **25.59** (beats Exp30); val 22.472 lost by 0.075; January still **35.16** vs 33.07.

## This fire
- **Exp77 DISCARD** CatBoost Ordered. Val 23.190 test 21.520. Axis closed: Ordered on 1h nowcast.
- **Exp78 DISCARD / NEAR-MISS** CatBoost Plain. Val 22.472 test 21.058. Hour-20 January fixed; overall January not.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual, Tweedie, Iws_delta, temp_delta, haze_hours6, reg_lambda=1, prev_SE/prev_cv, rain_mass, bagging_freq=1, drop lag13-24, MAE/quantile, doy_sin/doy_cos, heating_night / clock×heating, reg_alpha/L1, num_leaves<31, extra_trees min_data=50, anticyclone / PRES dummy, max_bin 127, extra_trees+linear bagging_freq=1
- t+6 open: rh_magnus + linear_lambda=1 (current recipe). persist>=250 typical over-clean still open.

## Process
LightGBM **50/50 complete**. CatBoost **4/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76. Snapshot `code_versions/catboost_start/`.

## Next pasteable
Stay on isolated **CatBoost Plain** (Exp78 near-miss). Next: Plain **lr=0.01** or **depth=4** on Exp30 features. Do not retry Ordered. Do not start MLP. Do not mix t+6 val with the 1h composite.
