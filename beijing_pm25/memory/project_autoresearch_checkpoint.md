# Autoresearch checkpoint — after Exp133 (1h still Exp97; t+6 recipe Exp76)

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
- **Exp 133** MLP batch 16 + wd=1e-4 + log_iws · val **22.502** · test **20.587** · January **31.13**

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** rain Ir>0 n=260 RMSE **24.80** vs CB **21.51** vs persist **27.27**, 4.8% of Exp130 SSE vs 3.5% of Exp97. Rainy high-Iws n=87 (mean Iws 30.4) **30.77** vs CB **24.06**, need **−11.29** pred_d **−3.89**. June rain n=28 need **−13.93** pred_d **−0.97**.
- **Exp133 DISCARD** 1h (val 22.502 vs Exp97 22.167). Val **22.502** beat Exp130 22.527 (new MLP val). Test 20.587. Rain 24.80→**23.59**. Rainy high-Iws 30.77→**29.04**.

## This fire
- **Exp133 DISCARD** 1h vs Exp97. MLP-side val KEEP vs Exp130. MLP **9/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)
- MLP patience=5 (do not retry 3 or another nearby shrink)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **9/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp133 recipe** (batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, lr 3e-4, log_iws). Change another unused **feature** next. Do not retry log-Iws, nearby patience, nearby epochs, batch 8, dropout 0.4, wd 1e-3, nearby lr shrink, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
