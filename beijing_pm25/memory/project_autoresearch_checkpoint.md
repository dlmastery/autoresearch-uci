# Autoresearch checkpoint — after Exp138 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 135** MLP batch 16 + log_iws + month_sin + pm25_accel · test **20.417** · val **22.350**

## MLP val recipe (not 1h champion)
- **Exp 136** MLP batch 16 + wd=1e-4 + log_iws + month_sin + pm25_accel + vent_index · val **22.259** · test **20.509** · January **30.96**

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** collapse hours with dPRES>=1 n=51 RMSE **86.12** vs CB **80.04** vs persist **107.64**, need **−91.41** pred_d **−24.29** (11.3% of Exp136 SSE). persist>=150 collapse n=35 RMSE **97.53** vs CB **88.82**.
- **Exp138 DISCARD** pres_delta. Val **22.438** missed Exp136 22.259. Test 20.440. Collapse dPRES>=1 86.12→**83.33**, pred_d −24.29→**−27.43** (right direction, still under-cleans 64). 2013 val inverted.

## This fire
- **Exp138 DISCARD** 1h vs Exp97. Pres_delta helped 2014 collapse slice but taxed 2013 val. MLP recipe remains Exp136. MLP **14/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)
- MLP patience=5 (do not retry 3 or another nearby shrink)
- MLP pm25_roll6max (do not retry roll3mean)
- MLP pres_delta (do not retry temp_delta or rh_delta)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **14/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp136 recipe** (batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, lr 3e-4, log_iws, month_sin, pm25_accel, vent_index). Change another unused **feature** next (e.g. evening_peak). Do not retry rolling PM stats, nearby weather derivatives, nearby products, nearby second-diff, month Fourier, log-Iws, nearby patience, nearby epochs, batch 8, dropout 0.4, wd 1e-3, nearby lr shrink, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
