# Autoresearch checkpoint — after Exp131 (1h still Exp97; t+6 recipe Exp76)

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
- **NEW:** hour 18 persist>=100 n=103 RMSE **32.58** vs CB **27.03** vs persist **36.50**, need **−1.04** pred_d **+1.82**. Hour 18 overall **26.99** vs CB **24.68** is **7.27%** of Exp130 SSE vs 5.91% of Exp97. February hour 18 **50.6** vs CB **37.5**. Val-test gap **2.07** vs CB **1.432**.
- **Exp131 DISCARD** epochs=80. Val **22.545** missed Exp130 22.527. Test 20.607. Hour-18 persist>=100 32.58→**32.23**. Hour 18 26.99→**26.76**.

## This fire
- **Exp131 DISCARD** 1h vs Exp97. Slower cosine barely moved evening tails. MLP recipe remains Exp130. MLP **7/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **7/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp130 recipe** (batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, lr 3e-4, epochs 50). Change unused **patience** next. Do not retry nearby epochs, batch 8, dropout 0.4, wd 1e-3, nearby lr shrink, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
