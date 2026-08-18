# Experiment summary — UCI 381 Beijing PM2.5 nowcast

Composite = `min(−val_RMSE, −test_RMSE) − 0.1 × n_RMSE>40`. KEEP iff composite rises. Test year 2014 is frozen.

**Champion:** Exp30 lightgbm · test RMSE **20.945** · val RMSE **22.397** · skill vs persistence **+6.1%**
**Campaign:** 61 experiments · 9 KEEP · 52 DISCARD
**Mandate gap:** LightGBM 35/50 · XGBoost 24/50 · CatBoost 2/50 · MLP 0/50 · FT-Transformer 0/50

## KEEP lineage

| Exp | Backbone | Delta | Test RMSE | Val RMSE | Composite |
|---:|---|---|---:|---:|---:|
| 1 | xgboost | baseline XGBoost nowcast, Chen-Guestrin 2016 defaults, frozen calendar split train2010-12/val2013/test2014 | 21.768 | 23.354 | -23.354 |
| 2 | xgboost | from champion: max_depth 4 | 21.996 | 23.205 | -23.205 |
| 4 | xgboost | from champion: learning_rate 0.01 | 22.008 | 23.124 | -23.124 |
| 8 | xgboost | from champion: subsample 0.6 | 22.034 | 22.983 | -22.983 |
| 14 | xgboost | from champion: add inversion_spread TEMP-DEWP | 21.823 | 22.885 | -22.885 |
| 15 | xgboost | from champion: add pm25_delta1 momentum | 21.290 | 22.684 | -22.684 |
| 22 | xgboost | from champion: stack inversion_spread onto delta champion | 21.122 | 22.470 | -22.470 |
| 29 | lightgbm | LightGBM on Exp22 inversion+delta features | 20.784 | 22.428 | -22.428 |
| 30 | lightgbm | LightGBM num_leaves 31 to 63 on Exp29 champion | 20.945 | 22.397 | -22.397 |

## All experiments

| Exp | Status | Backbone | Test RMSE | Val RMSE | Composite | MAE | R² |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | KEEP | xgboost | 21.768 | 23.354 | -23.354 | 11.722 | 0.9453 |
| 2 | KEEP | xgboost | 21.996 | 23.205 | -23.205 | 11.901 | 0.9441 |
| 3 | DISCARD | xgboost | 21.757 | 23.364 | -23.364 | 11.795 | 0.9453 |
| 4 | KEEP | xgboost | 22.008 | 23.124 | -23.124 | 11.903 | 0.9440 |
| 5 | DISCARD | xgboost | 22.012 | 23.208 | -23.208 | 11.892 | 0.9440 |
| 6 | DISCARD | xgboost | 21.697 | 23.142 | -23.142 | 11.904 | 0.9456 |
| 7 | DISCARD | xgboost | 22.008 | 23.124 | -23.124 | 11.903 | 0.9440 |
| 8 | KEEP | xgboost | 22.034 | 22.983 | -22.983 | 11.918 | 0.9439 |
| 9 | DISCARD | xgboost | 22.019 | 23.282 | -23.282 | 12.221 | 0.9440 |
| 10 | DISCARD | xgboost | 21.612 | 23.060 | -23.060 | 11.875 | 0.9460 |
| 11 | DISCARD | xgboost | 22.046 | 23.017 | -23.017 | 11.964 | 0.9439 |
| 12 | DISCARD | xgboost | 21.835 | 23.032 | -23.032 | 11.791 | 0.9449 |
| 13 | DISCARD | xgboost | 22.034 | 22.983 | -22.983 | 11.918 | 0.9439 |
| 14 | KEEP | xgboost | 21.823 | 22.885 | -22.885 | 11.933 | 0.9450 |
| 15 | KEEP | xgboost | 21.290 | 22.684 | -22.684 | 11.609 | 0.9476 |
| 16 | DISCARD | xgboost | 21.868 | 23.137 | -23.137 | 11.940 | 0.9448 |
| 17 | DISCARD | xgboost | 21.367 | 22.815 | -22.815 | 11.678 | 0.9473 |
| 18 | DISCARD | xgboost | 21.397 | 22.790 | -22.790 | 11.588 | 0.9471 |
| 19 | DISCARD | xgboost | 21.153 | 22.900 | -22.900 | 11.611 | 0.9483 |
| 20 | DISCARD | lightgbm | 21.050 | 22.810 | -22.810 | 11.560 | 0.9488 |
| 21 | DISCARD | catboost | 21.211 | 22.794 | -22.794 | 11.574 | 0.9480 |
| 22 | KEEP | xgboost | 21.122 | 22.470 | -22.470 | 11.545 | 0.9485 |
| 23 | DISCARD | xgboost | 21.252 | 22.727 | -22.727 | 11.633 | 0.9478 |
| 24 | DISCARD | xgboost | 21.348 | 22.651 | -22.651 | 11.591 | 0.9474 |
| 25 | DISCARD | lightgbm | 20.905 | 22.711 | -22.711 | 11.510 | 0.9495 |
| 26 | DISCARD | catboost | 21.248 | 22.969 | -22.969 | 11.589 | 0.9478 |
| 27 | DISCARD | xgboost | 21.081 | 22.488 | -22.488 | 11.556 | 0.9487 |
| 28 | DISCARD | xgboost | 21.182 | 22.563 | -22.563 | 11.590 | 0.9482 |
| 29 | KEEP | lightgbm | 20.784 | 22.428 | -22.428 | 11.478 | 0.9501 |
| 30 | KEEP | lightgbm | 20.945 | 22.397 | -22.397 | 11.550 | 0.9493 |
| 31 | DISCARD | lightgbm | 20.991 | 22.417 | -22.417 | 11.591 | 0.9491 |
| 32 | DISCARD | lightgbm | 20.949 | 22.621 | -22.621 | 11.598 | 0.9493 |
| 33 | DISCARD | lightgbm | 24.569 | 25.869 | -25.869 | 14.567 | 0.9303 |
| 34 | DISCARD | lightgbm | 81.461 | 80.885 | -81.561 | 54.784 | 0.2334 |
| 35 | DISCARD | lightgbm | 21.238 | 22.989 | -22.989 | 11.863 | 0.9479 |
| 36 | DISCARD | lightgbm | 21.127 | 22.662 | -22.662 | 11.617 | 0.9484 |
| 37 | DISCARD | lightgbm | 21.198 | 22.793 | -22.793 | 11.534 | 0.9481 |
| 38 | DISCARD | lightgbm | 20.987 | 22.426 | -22.426 | 11.535 | 0.9491 |
| 39 | DISCARD | lightgbm | 55.320 | 58.724 | -58.824 | 35.844 | 0.6465 |
| 40 | DISCARD | lightgbm | 20.939 | 22.439 | -22.439 | 11.580 | 0.9494 |
| 41 | DISCARD | lightgbm | 21.368 | 22.738 | -22.738 | 11.742 | 0.9473 |
| 42 | DISCARD | lightgbm | 20.956 | 22.515 | -22.515 | 11.582 | 0.9493 |
| 43 | DISCARD | lightgbm | 20.807 | 22.498 | -22.498 | 11.502 | 0.9500 |
| 44 | DISCARD | lightgbm | 20.912 | 22.471 | -22.471 | 11.508 | 0.9495 |
| 45 | DISCARD | lightgbm | 55.486 | 58.710 | -58.810 | 35.886 | 0.6443 |
| 46 | DISCARD | lightgbm | 55.337 | 58.365 | -58.465 | 35.942 | 0.6462 |
| 47 | DISCARD | lightgbm | 55.059 | 58.138 | -58.238 | 35.737 | 0.6498 |
| 48 | DISCARD | lightgbm | 54.648 | 58.359 | -58.459 | 35.338 | 0.6550 |
| 49 | DISCARD | lightgbm | 55.065 | 58.626 | -58.726 | 35.771 | 0.6497 |
| 50 | DISCARD | lightgbm | 55.090 | 58.259 | -58.359 | 35.744 | 0.6494 |
| 51 | DISCARD | lightgbm | 55.154 | 58.302 | -58.402 | 35.777 | 0.6486 |
| 52 | DISCARD | lightgbm | 55.053 | 58.323 | -58.423 | 35.867 | 0.6499 |
| 53 | DISCARD | lightgbm | 55.044 | 58.684 | -58.784 | 35.497 | 0.2404 |
| 54 | DISCARD | lightgbm | 54.790 | 58.672 | -58.772 | 35.318 | 0.6532 |
| 55 | DISCARD | lightgbm | 54.751 | 58.038 | -58.138 | 35.507 | 0.6537 |
| 56 | DISCARD | lightgbm | 54.487 | 57.658 | -57.758 | 35.279 | 0.6570 |
| 57 | DISCARD | lightgbm | 54.385 | 57.864 | -57.964 | 35.278 | 0.6583 |
| 58 | DISCARD | lightgbm | 54.540 | 57.704 | -57.804 | 35.299 | 0.6564 |
| 59 | DISCARD | lightgbm | 54.419 | 57.601 | -57.701 | 35.245 | 0.6579 |
| 60 | DISCARD | lightgbm | 54.324 | 57.849 | -57.949 | 35.143 | 0.6591 |
| 61 | DISCARD | lightgbm | 54.430 | 57.736 | -57.836 | 35.197 | 0.6577 |

## Champion residual slices (2014 test)

- Onset hours (Δ ≥ 50 µg/m³): n=95 RMSE=103.4 (pred 169 vs actual 248)
- Worst month: 01 RMSE=33.07
- Best month: 07 RMSE=13.60
- Worst hour: 20:00 RMSE=31.93
- Spike F1@75: 0.941 (P=0.933 R=0.949)
- p99 |error|=79.5 · max |error|=497.1
- Haze ≥150 n=1638: model 35.50 vs persist-1 35.31 (zero 1h skill)
- Persist-6 on same 7950 rows: **61.83**. Exp39 t+6 test **55.32** (skill +10.5%, 1h-gate DISCARD)
- Haze streaks ≥6h n=1069: model 29.31 vs persist-1 28.94 (loses inside episodes)
- High-PRES tercile skill +3.7% vs low-PRES +7.8%
- 2014 H1 skill +4.5% vs H2 +9.1%. Seed noise ≈ val ±0.08, test ±0.04 (Exp44)
- t+6 side ladder: persist-6 **61.83**. **Exp59 (Exp56 + cbwd_prev_NW) 54.42/57.60** (side-KEEP). Prior Exp56 54.49/57.66. Snapshot `code_versions/lightgbm_t6/`.
- t+6 actual≥200 n=944: model 101.2 **loses to persist-6 97.1**. Low-actual bias +30.3 / high-actual −34.0
- Exp47 need+100 n=286 predicted increment **+21 vs needed +146**. 76% of hours closer to mean 98 than persist.
- Exp53 persist-6 residual: test 55.044 val 58.684 (redundant, corr 0.990). Exp53 R²/MAPE are residual-scale.
- Exp54 Tweedie: test 54.790 val 58.672 side-MISS. Tail worse (actual≥200 105.4, need+100 increment +16.5).
- **Exp55 t+6 side-KEEP** (1h DISCARD): val 58.038 / test 54.751. dPRES>=1 increment flipped +3.05 → −1.90.
- **Exp56 t+6 side-KEEP** (1h DISCARD): val 57.658 / test 54.487. dewp_fall & not pres_rise increment flipped +3.14 → −0.22. actual≥200 99.57 vs persist 99.10. New t+6 recipe.
- Exp57 haze_hours6 side-MISS (val 57.864). Exp58 reg_lambda=1 side-MISS (val 57.704).
- **Exp59 t+6 side-KEEP** (1h DISCARD): val 57.601 / test 54.419. left-NW increment +9.11 → +5.69. New t+6 recipe.
- Exp60 rain_mass side-MISS (val 57.849). Ir>1 increment unchanged (+0.74).
- Exp61 bagging_freq=1 side-MISS (val 57.736). Late-dirty increment still +30.6.
