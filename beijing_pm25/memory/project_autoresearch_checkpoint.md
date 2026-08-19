# Autoresearch checkpoint — after Exp114 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** 2013 val persist RMSE **24.50** vs 2014 test **22.32** (2013 is harder). Exp97 skill **+9.5%** on val vs **+7.1%** on test. 2013 January persist **37.47** mean **166.8**, persist>=300 n=**138** vs 2014 n=39. 2013 February persist **38.30** vs 2014 **26.01**.
- **Exp114 is_janfeb:** val 22.342, test 20.792. January 34.84→35.02. Peak-heating flag did not help 2013 val.

## This fire
- **Exp114 DISCARD** is_janfeb. Test 20.792 val 22.342. Axis closed: Jan-Feb calendar subset of is_heating.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, Depthwise, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert), rh_iws, heating_build, pres_delta, min_data_in_leaf=20 (inert), early_stopping=50 (inert), pm25_delta6, log_iws, is_severe, evening_peak, rh_delta, temp_delta, se_iws, pm25_roll3mean, is_janfeb
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **40/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Do not retry month dummies / is_janfeb / roll3mean / se_iws / weather increments / lag1 flags / evening bins. 2013 val persist 24.50 is a harder year; Exp97 already +9.5% skill there. Leave Exp97 or regularize for 2013 without calendar subsets or bomb-chasing. Do not start MLP.
