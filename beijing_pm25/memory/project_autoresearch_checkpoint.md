# Autoresearch checkpoint — after Exp135 (1h still Exp97; t+6 recipe Exp76)

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
- **Exp 135** MLP batch 16 + wd=1e-4 + log_iws + month_sin + pm25_accel · val **22.350** · test **20.417** · January **30.92**

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** accel-q4 n=1941 (mean second-diff +26.4) is **31.5%** of Exp134 SSE, RMSE **23.22** vs CB **24.38** vs persist **25.11**, need **+1.11** pred_d **−0.02** (under-builds accelerating persist). Surprise onset accel<=0 n=35 **138.71** vs persist **133.37**.
- **Exp135 DISCARD** 1h (val 22.350 vs Exp97 22.167). Val **22.350** beat Exp134 22.432. Test **20.417** new 2014 best. Accel-q4 23.22→**23.13**, pred_d −0.02→**+0.32**.

## This fire
- **Exp135 DISCARD** 1h vs Exp97. MLP-side val KEEP vs Exp134. New best 2014 test. MLP **11/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)
- MLP patience=5 (do not retry 3 or another nearby shrink)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **11/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp135 recipe** (batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, lr 3e-4, log_iws, month_sin, pm25_accel). Change another unused **feature** next (e.g. vent_index). Do not retry nearby second-diff, month Fourier, log-Iws, nearby patience, nearby epochs, batch 8, dropout 0.4, wd 1e-3, nearby lr shrink, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
