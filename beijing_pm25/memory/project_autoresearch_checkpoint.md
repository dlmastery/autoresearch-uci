# Autoresearch checkpoint — after Exp164 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-20
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 164** MLP hidden 512-256-128 on Exp136 features · test **20.201** · val **22.180** (new 2014 best; MLP val best; 0.013 shy of Exp97 composite)
- **Exp 141** MLP batch 16 + log_iws + month_sin + pm25_accel + vent_index + pm25_delta6 · test **20.274** · val **22.356**
- **Exp 152** MLP dropout=0.1 on Exp136 recipe · test **20.277** · val **22.290**

## MLP val recipe (not 1h champion)
- **Exp 164** MLP hidden 512-256-128 + batch 16 + wd=1e-4 + log_iws + month_sin + pm25_accel + vent_index · val **22.180** · test **20.201** · January **31.90**
- Prior recipe Exp136 val 22.259 / test 20.509 is dominated on both splits.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** need>=30 build n=309 RMSE **65.12** vs persist **64.39** vs CB **64.51** (39.2% of Exp136 SSE; need +50.54 pred_d **+1.23** persist-locked jumps). Typical |need|<=10 already beats CB 7.21 vs 8.35.
- **Exp164 DISCARD** vs Exp97 (val 22.180 vs 22.167, Δ0.013). Beats Exp136 val **22.259→22.180** and test **20.509→20.201**. Builds 65.12→**65.98** inverted. |need|>=80 135.18→**128.15** beats CB. Typical 7.21→**7.53**. January 30.96→**31.90**.
- Do not nearby-widen 384/768. MLP recipe updates to Exp164.

## This fire
- **Exp164 DISCARD** 1h vs Exp97 (near-miss 0.013). New best 2014 test and new best MLP val. MLP **40/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP dropout=0.1 (do not retry 0.05 or 0.15)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP extra hidden 256-128-64-32 (do not retry 5-layer or nearby 4th-layer width 16/64)
- MLP hidden 512-256-128 (do not retry nearby 384/768 or another 3-layer widen)
- MLP hetero_loss (do not retry another aleatoric-head or nearby heteroscedastic loss)
- MLP grad_clip=0 (do not retry nearby clip 0.1/5/10)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP Adam lr=1e-3 (do not retry 5e-4 or 2e-3)
- MLP batch_size=64 (do not retry nearby 48 or 128)
- MLP weight_decay=0 (do not retry nearby 1e-6)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)
- MLP patience=5 (do not retry 3 or another nearby shrink)
- MLP pm25_roll6max (do not retry roll3mean)
- MLP pres_delta (do not retry temp_delta or rh_delta)
- MLP evening_peak (do not retry is_morning or heating_night)
- MLP se_iws (do not retry nw_iws)
- MLP pm25_delta6 (do not retry another 6h PM slope)
- MLP is_severe (do not retry another lag1 threshold dummy)
- MLP cbwd_prev_NW (do not retry Iws_lag1 or another previous-direction dummy)
- MLP is_janfeb (do not retry another is_heating split)
- MLP iws_clip100 (do not retry another Iws transform)
- MLP dow_sin (do not retry dow_cos)
- MLP cv_inv (do not retry another calm or inversion product)
- MLP heating_build (do not retry heating_night or another heating product)
- MLP rh_iws (do not retry another RH/wind ratio)
- MLP drop Iws (do not retry dropping log_iws)
- MLP drop Is (do not retry drop Ir; rain under-cleans)
- MLP drop PRES (do not retry drop TEMP or DEWP)
- MLP drop is_weekend (do not retry drop dow)
- MLP drop inversion_spread (do not retry drop rh_magnus or vent_index)
- MLP drop is_heating (do not retry drop month_sin)
- MLP drop cbwd_cv (do not retry drop cbwd_NE/NW/SE)
- Exp136 extra-feature adds (137–147 plus heating_build, rh_iws) exhausted
- MLP extra depth (Exp148) exhausted
- MLP HP opposites (lr, dropout, batch, wd) exhausted
- Drop-raw-weather (Iws, Is, PRES) exhausted — rethink, not another weather drop
- Collinear-derived drops (is_weekend, inversion_spread, is_heating) exhausted — rethink, not another derived copy

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **40/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp164 recipe** (batch 16, hidden 512-256-128, dropout 0.2, weight_decay 1e-4, lr 3e-4, clip=1.0, log_iws, month_sin, pm25_accel, vent_index). Next unused axis: diagnose Exp164 builds (need>=30 still pred_d +0.97 vs need +50.54) — **not** nearby widen 384/768, extra 4th layer, or dropout 0.1. Do not retry drop cbwd_cv, drop is_heating, drop month_sin, drop inversion_spread, drop rh_magnus, drop vent_index, drop is_weekend, drop dow, drop PRES, drop TEMP, drop Is, drop Ir, drop Iws, rh_iws, heating_build, extra hidden 32, 5-layer, nearby 4th-layer width, aleatoric heads, nearby clip 0.1/5/10, rolling PM stats, 6h PM slopes, lag1 thresholds, previous-direction memory, calendar splits of is_heating, Iws transforms, cyclic weekday encodings, nearby weather derivatives, nearby hour bins, nearby wind products, nearby second-diff, month Fourier, log-Iws, nearby patience, nearby epochs, batch 8/48/64/128, dropout 0.4/0.05/0.15, wd 1e-3/0/1e-6, nearby lr shrink/raise, heating products, drop log_iws, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
