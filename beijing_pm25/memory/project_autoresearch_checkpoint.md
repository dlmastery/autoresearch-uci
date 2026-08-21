# Autoresearch checkpoint — after Exp177 DISCARD (1h remains Exp167 residual MLP; FT 3/50; t+6 recipe Exp76)

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
- **NEW:** typical |need|<=10 and |pred_d|>=5 n=1514 RMSE **10.54** vs persist **5.48** (5.26% of SSE; need **+0.89** pred_d **+0.93**). Residual MLP already over-moves 1514 calm hours.
- **Exp177 DISCARD** FT n_layers=2. Val **23.222** missed 21.972 (inside 22.10–25.20) and missed Exp175 22.698. Test **23.513**. Typical |pred_d|>=5 10.54→**16.72** vs Exp175 16.48 (no lift). Typical 7.14→**10.41**. Dirty-stable 11.99→**25.05**. January 31.22→**42.05**. Onset pred_d −0.60→**−7.61**. Middle depth interpolated 1 and 3; persist stayed buried. **FT depth axis closed (3 DISCARDs).**

## This fire
- **Exp177 DISCARD** FT n_layers=2 (isolated cycle 3/50). 1h champion remains Exp167. FT **3/50**. Depth {1,2,3} exhausted — rethink architecture, not n_layers=4.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT-Transformer Gorishniy 2021 paper default d_model=64 n_layers=3 batch=32 lr=1e-4 (do not retry nearby d_model 32/96 or n_heads 2/8 as a persist fix)
- FT n_layers=1 (do not retry n_layers=0 or another nearby shrink to a token-linear CLS)
- FT n_layers=2 (do not retry n_layers=4/6; depth axis closed after 3 DISCARDs)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **3/50**. Isolation holds. 1h champion is **Exp167 residual MLP**. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (3/50) on the Exp167 feature recipe. Depth {1,2,3} closed — rethink architecture: **Pre-LN (norm_first=True)** on the paper-default 3-layer FT, not n_layers=4. Do not mix MLP HPs into FT. Do not retry d_model 32/96. 1h champion remains Exp167 until composite beats −21.972.
