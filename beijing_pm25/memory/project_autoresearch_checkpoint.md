# Autoresearch checkpoint — after Exp42 (still Exp30)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persistence **+6.15%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, L2 gbdt, max_bin 255, 1h nowcast
- features: base + `pm25_delta1` + `inversion_spread`

## Residual (this fire: PRES / haze streaks)
- High-PRES tercile n=2500 skill only **+3.7%** (RMSE 22.97 vs persist 23.86); low-PRES **+7.8%**
- Haze streaks ≥6h: n=1069 **model 29.31 vs persist-1 28.94** (loses inside established episodes)
- Onset n=83 model 110.05 vs persist-1 107.80
- January 33.07 vs JJA 14.03 · Hour 20 31.93 · April 9 n=24 RMSE 120.81
- Val is the 1h bottleneck (22.397 vs test 20.945)

## This fire
- **Exp41 DISCARD** Ke max_bin=127. Val 22.738 test 21.368. Coarser histograms hurt.
- **Exp42 DISCARD** pm25_roll6max. Val 22.515 test 20.956. Redundant with lag1–6.

## Exhausted / closed
- Do not retry depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}
- Axis closed: GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, pm25_accel, vent_index, max_bin=127, roll6max/mean/min, treating t+6 RMSE as a 1h KEEP

## Process
LightGBM **16/50**. Isolation holds. Champion unchanged.
Side ladder still open: Exp39 t+6 test 55.32 vs persist-6 61.83.

## Next pasteable
Stop shaving 1h regularizers/pools. Hillclimb **t+6 from Exp39** vs persist-6 as a separate composite, or multi-seed variance on Exp30. Do not start CatBoost/MLP.
