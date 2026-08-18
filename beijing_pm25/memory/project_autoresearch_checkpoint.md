# Autoresearch checkpoint — after Exp68 (1h still Exp30; t+6 recipe Exp68)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 68** LightGBM 31 leaves + extra_trees + month_sin + pres_delta + dewp_delta + cbwd_prev_NW · test **54.482** · val **57.498**
- vs persist-6 **61.83** skill **+11.9%**
- prior Exp59 54.419 / 57.601
- snapshot: `code_versions/lightgbm_t6/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05
- **Exp59 new slices:** SE collapse n=271 need **−107.1** pred **−21.2**. SE-night collapse n=162 RMSE **111.04** need **−106.4** pred **−12.9**. SE dirty Iws-down skill **+5.4%**.
- **Exp68:** SE-night increment still **−13.0**. January RMSE 83.79 → **82.95**. Val paid.

## This fire
- **Exp68** 1h DISCARD, **t+6 side-KEEP** extra_trees. Val 57.498 beat 57.601, test 54.482. New t+6 recipe.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual, Tweedie, Iws_delta, temp_delta, haze_hours6, reg_lambda=1, prev_SE/prev_cv, rain_mass, bagging_freq=1, drop lag13-24, MAE/quantile, doy_sin/doy_cos, heating_night / clock×heating, reg_alpha/L1, num_leaves<31

## Process
LightGBM **42/50**. Isolation holds. 1h champion unchanged. t+6 recipe is now Exp68 extra_trees.

## Next pasteable
Stay on **Exp68**. SE-night collapse still predicts −13 vs need −106. Do not retry extra_trees off / leaves<31 / jan_evening / doy_cos. Fill remaining LGB 8. Do not start CatBoost/MLP until LGB 50 or `lightgbm_final`.
