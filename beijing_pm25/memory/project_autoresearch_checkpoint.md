# Autoresearch checkpoint — after Exp76 (1h still Exp30; t+6 recipe Exp76)

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
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05
- **Exp72 new slices:** persist>=250 typical n=237 RMSE **82.39** vs persist-6 **28.27** (skill **−191.5%**), need **−0.1**, pred **−51.5**. Hour 22 RMSE **65.19**. RH 70-85 persist>=150 skill only **+4.8%**.
- **Exp75:** val **57.191** side-KEEP. Hour-6 blow-up RMSE **67.07**, one RH=100 row pred **872** vs actual **116**.
- **Exp76:** hour-6 **53.55**, blow-up row **132**. persist>=250 typical still pred **−52.7** vs need **−0.1**.

## This fire
- **Exp75 t+6 side-KEEP** rh_magnus. Val 57.191 beat 57.429, test 54.730. 1h DISCARD.
- **Exp76 t+6 side-KEEP** linear_lambda=1. Val 57.161 beat 57.191, test 54.312. 1h DISCARD. Hour-6 bomb closed.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual, Tweedie, Iws_delta, temp_delta, haze_hours6, reg_lambda=1, prev_SE/prev_cv, rain_mass, bagging_freq=1, drop lag13-24, MAE/quantile, doy_sin/doy_cos, heating_night / clock×heating, reg_alpha/L1, num_leaves<31, extra_trees min_data=50, anticyclone / PRES dummy, max_bin 127, extra_trees+linear bagging_freq=1
- t+6 open: rh_magnus + linear_lambda=1 (current recipe). persist>=250 typical over-clean still open.

## Process
LightGBM **50/50 complete**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe is Exp76. Snapshot `code_versions/lightgbm_final/`.

## Next pasteable
LightGBM cycle is done. Next isolated cycle: **CatBoost** (2/50 so far). Do not mix t+6 val with the 1h composite. Do not retry bagging / max_bin / another RH formula. persist>=250 typical still predicts −53 vs need 0 on Exp76.
