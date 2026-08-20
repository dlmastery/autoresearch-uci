# Autoresearch checkpoint — after Exp132 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 130** MLP batch_size=16 · test **20.457** · val **22.527**

## MLP val recipe (not 1h champion)
- **Exp 130** MLP batch 16 + wd=1e-4 · val **22.527** · test **20.457** · January **30.90**

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** hour 13 n=333 RMSE **17.98** vs CB **16.22** vs persist **19.99**, need **−1.41** pred_d **−2.30** (over-cleans midday). January hour 13 **26.2** vs CB **20.4**. April hour 13 pred_d **−7.1** vs need **−2.0**. JJA **14.15** vs CB **13.84**.
- **Exp132 DISCARD** patience=5. Val **22.757** missed Exp130 22.527. Test 20.764. Hour 13 17.98→**18.09**. Train time 143s→73s (did stop earlier). Hypothesis inverted (underfit).

## This fire
- **Exp132 DISCARD** 1h vs Exp97. Earlier stop underfit 2013. MLP recipe remains Exp130. MLP **8/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)
- MLP patience=5 (do not retry 3 or another nearby shrink)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **8/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp130 recipe** (batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, lr 3e-4, epochs 50, patience 10). Change an unused **feature** next (hour-13 / rain tails). Do not retry nearby patience, nearby epochs, batch 8, dropout 0.4, wd 1e-3, nearby lr shrink, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
