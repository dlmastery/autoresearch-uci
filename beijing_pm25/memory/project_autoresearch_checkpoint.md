# Autoresearch checkpoint — after Exp192 KEEP (1h now Exp192 FT; FT 18/50; t+6 Exp76)

**Updated:** 2026-08-22
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 192** FT-Transformer Pre-LN +cbwd_prev_NW +rh_iws · composite **−21.948** · 2014 test RMSE **20.453** · 2013 val **21.948**
- skill vs persist-1 **+8.35%** · 1h noise floor val ±0.08
- Recipe: Exp167 features + cbwd_prev_NW + rh_iws · d_model 64 · n_heads 4 · n_layers 3 · dropout 0.1 · lr 1e-4 · batch 32 · weight_decay 1e-5 · warmup 10 · epochs 100 · patience 15 · norm_first true
- First FT KEEP versus Exp167. First FT-Transformer to hold the frozen 2014 composite.

## Best 2014 test (not the champion)
- **Exp 167** residual MLP · test **20.072** · val **21.972** · composite **−21.972** (now second)
- Best non-champion 2014 test: Exp172 stagn_onset **20.018** (val 21.9995 DISCARD near-miss)
- Best prior FT test: Exp187 +heating_night **20.350** (val 22.221 DISCARD)
- Prior FT val recipe: Exp186 Pre-LN +cbwd_prev_NW **22.066** / test **20.483** (now superseded by Exp192)

## MLP val recipe
- **Exp 167** residual MLP · val **21.972** · test **20.072**. Isolated; do not mix MLP HPs into FT.

## FT val recipe (now the 1h champion)
- **Exp 192** Pre-LN + cbwd_prev_NW + rh_iws · dropout 0.1 · n_layers 3 · d_model 64 · batch 32 · lr 1e-4 · weight_decay 1e-5 · warmup 10 · val **21.948** · test **20.453**
- Beat Exp167 val 21.972 / composite −21.972 (Δ composite +0.024). Test 20.453 missed Exp167 20.072 but beat Exp186 20.483.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- Champion slices (Exp192, computed): January 33.22 vs persist 33.58 · JJA 14.12 vs persist 14.83 · hour 20 32.69 vs persist 33.24 · onset n=83 RMSE 110.79 vs persist 107.80 (need +87.40 pred_d −1.54). Val 21.948 vs test 20.453 is still the bottleneck.
- Targeted slice heating RH>=70 Iws<5 persist>=80 n=245 RMSE **33.54** vs persist **31.57** (need **+0.86** pred_d **−3.84**) vs Exp167 31.59 / −1.09 — over-clean worsened. KEEP is val-side, not the moist-calm bomb.
- Typical 7.54 vs Exp167 7.14. Global bias **−0.07** vs Exp167 −0.29 vs Exp186 −2.04.

## This fire
- **Exp192 KEEP** FT Pre-LN add rh_iws on Exp186 (isolated cycle 18/50). 1h champion is now Exp192. FT **18/50**. FT val recipe is Exp192.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT Post-LN depth {1,2,3} closed (do not retry n_layers=4/6 or revert Post-LN)
- FT paper-default d_model 32/96 / n_heads 2/8 as a persist fix closed
- FT Pre-LN dropout={0, 0.2} (do not retry nearby 0.05/0.15/0.3)
- FT Pre-LN batch_size=64 (do not retry nearby 48/128)
- FT Pre-LN weight_decay=1e-4 (do not retry nearby 5e-5/2e-4/0)
- FT Pre-LN lr=3e-4 (do not retry nearby 2e-4/5e-4)
- FT Pre-LN warmup=0 (do not retry nearby 2/5)
- FT Pre-LN warmup=20 (do not retry nearby 15/25). Warmup axis closed {0,20}; recipe 10 stays.
- FT heating_night token (do not retry heating_build)
- FT pres_delta token (do not retry temp_delta/rh_delta)
- FT is_morning token (do not retry evening_peak)
- FT pm25_roll3mean (do not retry pm25_roll6max)
- FT iws_clip100 (do not retry other Iws clips)
- Do not drop rh_iws or cbwd_prev_NW from Exp192

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **18/50**. Isolation holds. 1h champion is **Exp192 FT Pre-LN +rh_iws**. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (18/50) from the Exp192 Pre-LN + cbwd_prev_NW + rh_iws recipe. Next try **add se_iws**. Do not drop rh_iws or cbwd_prev_NW. Do not retry heating_night/pres_delta/is_morning/evening_peak/pm25_roll3mean/iws_clip100. Do not retry warmup 15/25. Do not retry lr 2e-4/5e-4. Do not retry wd 5e-5/2e-4/0. Do not retry batch 48/64/128. Do not retry dropout 0/0.2. Do not revert Post-LN. Do not mix MLP HPs. 1h champion remains Exp192 until composite beats −21.948.
