# Autoresearch checkpoint — after Exp123 (1h still Exp97; t+6 recipe Exp76)

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
- **NEW:** corr(dow_sin, y) val **−0.078** vs 2011 **+0.051** vs 2012 **−0.046**. Numeric dow corr val 0.065 vs train ~0. Test residual corr with dow_sin **−0.027**. Thursday still loses persist 20.85 vs 20.75.
- **Exp123 DISCARD** dow_sin. Val **22.360** test **20.829**. Thursday 20.85→**21.31**. Cyclic weekday taxed val more than drop-dow (22.212).

## This fire
- **Exp123 DISCARD** dow_sin. Test 20.829 val 22.360. Axis closed: cyclic weekday (dow_sin / dow_cos).

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, Depthwise, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert), rh_iws, heating_build, pres_delta, min_data_in_leaf=20 (inert), early_stopping=50 (inert), pm25_delta6, log_iws, is_severe, evening_peak, rh_delta, temp_delta, se_iws, pm25_roll3mean, is_janfeb, drop lag13-24, iws_clip100, drop dow, model_size_reg=1.0 (inert), Bernoulli subsample=0.8, border_count=128, nw_iws, is_morning, dow_sin
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **49/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Do not retry dow_sin / dow_cos / hour-bin dummies / wind×Iws / border_count {64,128} / Bernoulli subsample / model_size_reg {1.0, 2.0} / drop dow / drop is_weekend / Iws clips / drop lag7-12 / month dummies / roll3mean / se_iws / weather increments / lag1 flags / evening bins. Keep numeric dow, is_weekend, hour_sin/hour_cos. Last CatBoost slot (50/50): leave Exp97 or one unused feature that is not cyclic weekday, hour bins, wind-speed products, or unused regularizer HPs. Do not start MLP until CatBoost 50/50.
