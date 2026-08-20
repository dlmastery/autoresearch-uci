# Autoresearch checkpoint — after Exp150 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-20
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 141** MLP batch 16 + log_iws + month_sin + pm25_accel + vent_index + pm25_delta6 · test **20.274** · val **22.356**

## MLP val recipe (not 1h champion)
- **Exp 136** MLP batch 16 + wd=1e-4 + log_iws + month_sin + pm25_accel + vent_index · val **22.259** · test **20.509** · January **30.96**

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** rain persist>=100 n=79 RMSE **38.52** vs CB **33.16** vs persist **44.20**, need **−14.53** pred_d **−8.62** (3.5% of Exp136 SSE; clip=1.0 under-washes). Ir>0 24.06 vs CB 21.51.
- **Exp150 DISCARD** grad_clip=0. Val **22.402** missed Exp136 22.259. Test **20.400** (beat Exp136). rain persist>=100 38.52→**39.15** flat. Crash 86.06→**80.40** now beats CB. Typical 7.21→7.50.

## This fire
- **Exp150 DISCARD** 1h vs Exp97. Unclipped AdamW helped crash/collapse and 2014 test but taxed rain and 2013 val. MLP **26/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP extra hidden 256-128-64-32 (do not retry 5-layer or nearby 4th-layer width 16/64)
- MLP hetero_loss (do not retry another aleatoric-head or nearby heteroscedastic loss)
- MLP grad_clip=0 (do not retry nearby clip 0.1/5/10)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
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
- Exp136 extra-feature adds (137–147) exhausted
- MLP extra depth (Exp148) exhausted

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **26/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp136 recipe** (batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, lr 3e-4, clip=1.0, log_iws, month_sin, pm25_accel, vent_index). Next unused axis: **Adam lr=1e-3** (unused opposite of 1e-4), not grad_clip, hetero_loss, extra depth, or another feature. Do not retry extra hidden 32, 5-layer, nearby 4th-layer width, aleatoric heads, nearby clip 0.1/5/10, rolling PM stats, 6h PM slopes, lag1 thresholds, previous-direction memory, calendar splits of is_heating, Iws transforms, cyclic weekday encodings, nearby weather derivatives, nearby hour bins, nearby wind products, nearby second-diff, month Fourier, log-Iws, nearby patience, nearby epochs, batch 8, dropout 0.4, wd 1e-3, nearby lr shrink, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
