# Autoresearch checkpoint — after Exp84 (1h still Exp30; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**
- CatBoost t+6 Exp81 test **53.929** / val **57.857** (test win, val miss)
- snapshot: `code_versions/lightgbm_t6/` and `code_versions/lightgbm_final/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · pred +0.2 vs need +87.4 · val bottleneck
- **NEW Exp81:** January **82.18** vs Exp76 **80.40**. RH<40 **47.28** vs **46.72**. RH>=85 **56.25** vs **55.53**. RH 40-70 is the only CatBoost win (**56.00** vs **57.44**).
- **Exp83:** bagging_temperature=2 **bit-identical** to Exp81 (inert).
- **Exp84:** drop rh_magnus val **58.075** / test **54.155**. RH<40 **47.49** worse.

## This fire
- **Exp83 DISCARD** bagging_temperature=2. No-op vs Exp81. Axis closed: T=2 on Plain.
- **Exp84 DISCARD** drop rh_magnus. Val 58.075 test 54.155. Axis closed: drop RH.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **10/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost**. Best 1h CatBoost is Exp78 Plain depth6 lr=0.03. CatBoost t+6 Exp81 still best test (53.93) and still loses val. Next: **random_strength** (wired, unused) or return to 1h Exp78. Do not retry bagging_temperature / l2=10 / drop rh_magnus / Ordered / lr 0.01 / depth 4. Do not start MLP.
