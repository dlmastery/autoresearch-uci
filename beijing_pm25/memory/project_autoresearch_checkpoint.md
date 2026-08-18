# Autoresearch checkpoint — after Exp67 (1h still Exp30; t+6 recipe Exp59)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 59** LightGBM 31 leaves + month_sin + pres_delta + dewp_delta + cbwd_prev_NW · test **54.419** · val **57.601**
- vs persist-6 **61.83** skill **+12.0%**
- snapshot: `code_versions/lightgbm_t6/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05
- **Exp59 new slices:** typical |need|<=50 n=5941 RMSE **29.28** vs persist-6 **23.36** (skill **−25.3%**). Typical persist>=150 n=731 RMSE **54.25** vs persist-6 **28.31**, need **−0.7**, pred **−20.4**. February typical 45.86 vs persist-6 23.54.
- **Exp67:** typical P>=150 increment still **−20.4**.

## This fire
- **Exp67 DISCARD** num_leaves 15. Val 57.916 test 54.424. Axis closed: t+6 leaves below 31.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual, Tweedie, Iws_delta, temp_delta, haze_hours6, reg_lambda=1, prev_SE/prev_cv, rain_mass, bagging_freq=1, drop lag13-24, MAE/quantile, doy_sin/doy_cos, heating_night / clock×heating, reg_alpha/L1, num_leaves<31

## Process
LightGBM **41/50**. Isolation holds. 1h champion unchanged. t+6 recipe remains Exp59.

## Next pasteable
Stay on **Exp59**. Typical dirty hours still predict −20 vs need 0 after cutting to 15 leaves. Do not retry num_leaves 21 / leaf L1-L2 / jan_evening / doy_cos. Fill remaining LGB 9. Do not start CatBoost/MLP until LGB 50 or `lightgbm_final`.
