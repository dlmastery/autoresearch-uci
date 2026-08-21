# Autoresearch checkpoint — after Exp176 DISCARD (1h remains Exp167 residual MLP; FT 2/50; t+6 recipe Exp76)

**Updated:** 2026-08-21
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 167** MLP residual skips · composite **−21.972** · 2014 test RMSE **20.072** · 2013 val **21.972**
- skill vs persist-1 **+10.06%** · 1h noise floor val ±0.08
- Recipe: Exp136 features + hidden 512-256-128 + residual projection shortcuts · batch 16 · dropout 0.2 · wd=1e-4 · lr 3e-4 · clip=1.0 · layer_norm off · huber_beta=1 · persist_residual off · underpred_weight off
- First 1h KEEP since Exp97. First MLP to beat CatBoost on the frozen 2014 composite.

## Best 2014 test (now the champion)
- **Exp 167** residual MLP · test **20.072** · val **21.972**
- Best non-champion 2014 test: Exp172 stagn_onset **20.018** (val 21.9995 DISCARD near-miss)
- Prior: Exp164 20.201 / 22.180 · Exp141 20.274 / 22.356 · Exp152 20.277 / 22.290

## MLP val recipe
- **Exp 167** is both 1h champion and MLP val recipe.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- Champion slices (Exp167, computed): January 31.22 vs persist 33.58 · JJA 13.87 vs persist 14.83 · hour 20 32.68 vs persist 33.24 (11.10% of SSE) · onset n=83 RMSE 110.28 vs persist 107.80 (31.51% of SSE; need +87.40 pred_d −0.60). Val 21.972 vs test 20.072 is the bottleneck.
- **NEW:** heating dirty-stable persist>=150 |need|<=10 n=269 RMSE **15.66** vs persist **6.19** (2.06% of SSE; need **−0.09** pred_d **−4.08**). Residual MLP already over-cleans stagnant heating hours.
- **Exp176 DISCARD** FT n_layers=1. Val **25.443** missed 21.972 (outside 21.80–24.20). Test **25.954** missed persist 22.316 and Exp175 23.130. Heating dirty-stable 15.66→**44.22** vs Exp175 35.80; pred_d −4.08→**−14.08**. Typical 7.14→**12.12**. Dirty-stable 11.99→**30.31**. January 31.22→**48.70**. Onset pred_d −0.60→**−14.70**. One layer underfit and buried lag-1 more.

## This fire
- **Exp176 DISCARD** FT n_layers=1 (isolated cycle 2/50). 1h champion remains Exp167. FT **2/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT-Transformer Gorishniy 2021 paper default d_model=64 n_layers=3 batch=32 lr=1e-4 (do not retry nearby d_model 32/96 or n_heads 2/8 as a persist fix)
- FT n_layers=1 (do not retry n_layers=0 or another nearby shrink to a token-linear CLS)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **2/50**. Isolation holds. 1h champion is **Exp167 residual MLP**. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (2/50) on the Exp167 feature recipe. Next try **n_layers=2** (unused middle depth; 1 underfit worse than 3). Do not mix MLP HPs into FT. Do not retry n_layers=1/0 or paper-default d_model 32/96. 1h champion remains Exp167 until composite beats −21.972.
