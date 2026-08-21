# Autoresearch checkpoint — after Exp178 DISCARD (1h remains Exp167 residual MLP; FT 4/50 Pre-LN val recipe; t+6 recipe Exp76)

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
- Best FT: Exp178 Pre-LN test **20.674** · val **22.140**
- Prior: Exp164 20.201 / 22.180 · Exp141 20.274 / 22.356 · Exp152 20.277 / 22.290

## MLP val recipe
- **Exp 167** is both 1h champion and MLP val recipe.

## FT val recipe (isolated, not champion)
- **Exp 178** Pre-LN (norm_first=true) · n_layers 3 · d_model 64 · batch 32 · lr 1e-4 · val **22.140** · test **20.674**
- Beats persist 22.316 on 2014. Missed Exp167 composite by val Δ0.168.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- Champion slices (Exp167, computed): January 31.22 vs persist 33.58 · JJA 13.87 vs persist 14.83 · hour 20 32.68 vs persist 33.24 (11.10% of SSE) · onset n=83 RMSE 110.28 vs persist 107.80 (31.51% of SSE; need +87.40 pred_d −0.60). Val 21.972 vs test 20.072 is the bottleneck.
- **NEW:** dirty-stable NW persist>=150 |need|<=10 n=156 RMSE **17.54** vs persist **6.18** (1.50% of SSE; need **−0.08** pred_d **−9.17**). Residual MLP subtracts 9 µg on already-dirty NW hours.
- **Exp178 DISCARD** FT Pre-LN. Val **22.140** missed 21.972 (beat Exp175 Post-LN 22.698). Test **20.674** beat persist 22.316 and Exp175 23.130. Dirty-stable NW 17.54→**20.63** vs Post-LN 33.82; pred_d −9.17→**−9.41** vs Post-LN −14.17. Typical 7.14→**7.96** vs Post-LN 10.22. January 31.22→**34.77** vs Post-LN 42.85. Onset pred_d −0.60→**−0.94** vs Post-LN −6.95. Pre-LN restored lag-1 versus Post-LN; did not beat residual MLP.

## This fire
- **Exp178 DISCARD** FT Pre-LN (isolated cycle 4/50). 1h champion remains Exp167. FT **4/50**. Pre-LN is the FT val recipe.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT-Transformer Gorishniy 2021 paper default d_model=64 n_layers=3 batch=32 lr=1e-4 Post-LN (do not retry nearby d_model 32/96 or n_heads 2/8 as a persist fix)
- FT n_layers={1,2,3} Post-LN depth axis closed (do not retry n_layers=4/6)
- FT Post-LN (do not revert norm_first=false)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **4/50**. Isolation holds. 1h champion is **Exp167 residual MLP**. FT val recipe is Exp178 Pre-LN. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (4/50) from the Exp178 Pre-LN recipe (norm_first=true, n_layers=3). Next try **dropout=0**. Do not revert Post-LN. Do not retry n_layers=4 or d_model 32/96 as a persist fix. Do not mix MLP HPs. 1h champion remains Exp167 until composite beats −21.972.
