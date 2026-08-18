# Autoresearch checkpoint — after Exp44 (still Exp30)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persistence **+6.15%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, **bagging_freq 0 (bagging is a no-op)**, seed 0
- features: base + `pm25_delta1` + `inversion_spread`

## Residual (this fire: H1/H2, collapse, error AC)
- Jan–Jun 2014 n=3953 skill only **+4.5%** (RMSE 24.17); Jul–Dec **+9.1%** (17.17)
- Hour 20 RMSE 31.93 vs morning 07–09 **18.28**
- Onset n=83 model 110.05 vs persist-1 107.80
- Collapse n=162 model **74.59 vs persist 97.87** (helps drops)
- |error| AC1 **0.38**; signed error AC1 ≈ 0
- Val is the 1h bottleneck (22.397 vs test 20.945)

## This fire
- **Exp43 DISCARD** bagging_freq=1 (enables the 0.6 fraction). Test **20.807** (best since Exp29) val 22.498. Val gate failed.
- **Exp44 DISCARD** seed=1. Val 22.471 (+0.074) test 20.912 (−0.033). Inside predicted noise band.

## Noise floor
1h seed noise ≈ **val ±0.08**, **test ±0.04**. Near-misses smaller than that are not KEEP signal.

## Exhausted / closed
- Do not retry depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}
- Axis closed: GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, pm25_accel, vent_index, max_bin=127, roll6max, bagging_freq=1, seed swaps, treating t+6 RMSE as a 1h KEEP

## Process
LightGBM **18/50**. Isolation holds. Champion unchanged.
Framework `gbm.py` now accepts `bagging_freq` (default 0). Side ladder: Exp39 t+6 test 55.32 vs persist-6 61.83.

## Next pasteable
Hillclimb **t+6 from Exp39** vs persist-6 as a **separate** composite. Do not shave 1h HPs inside the 0.08 val noise. Do not start CatBoost/MLP.
