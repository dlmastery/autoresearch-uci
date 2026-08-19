# Experiment summary — UCI 381 Beijing PM2.5 nowcast

Composite = `min(−val_RMSE, −test_RMSE) − 0.1 × n_RMSE>40`. KEEP iff composite rises. Test year 2014 is frozen.

**Champion:** Exp97 catboost · test RMSE **20.735** · val RMSE **22.167** · skill vs persistence **+7.1%**
**Campaign:** 104 experiments · 11 KEEP · 93 DISCARD
**Mandate gap:** LightGBM 50/50 · XGBoost 24/50 · CatBoost 30/50 · MLP 0/50 · FT-Transformer 0/50

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
| 96 | catboost | CatBoost Plain add dewp_delta on Exp91 rh_magnus (CatBoost cycle 22/50) | 20.881 | 22.357 | -22.357 |
| 97 | catboost | CatBoost Plain add is_heating on Exp96 dewp_delta (CatBoost cycle 23/50) | 20.735 | 22.167 | -22.167 |

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
| 62 | DISCARD | lightgbm | 53.835 | 58.051 | -58.151 | 34.978 | 0.6652 |
| 63 | DISCARD | lightgbm | 54.350 | 58.798 | -58.898 | 34.068 | 0.6588 |
| 64 | DISCARD | lightgbm | 54.135 | 58.053 | -58.153 | 35.149 | 0.6614 |
| 65 | DISCARD | lightgbm | 54.322 | 57.649 | -57.749 | 35.151 | 0.6591 |
| 66 | DISCARD | lightgbm | 54.454 | 57.719 | -57.819 | 35.215 | 0.6574 |
| 67 | DISCARD | lightgbm | 54.424 | 57.916 | -58.016 | 35.466 | 0.6578 |
| 68 | DISCARD | lightgbm | 54.482 | 57.498 | -57.598 | 35.309 | 0.6571 |
| 69 | DISCARD | lightgbm | 54.425 | 57.620 | -57.720 | 35.292 | 0.6578 |
| 70 | DISCARD | lightgbm | 54.620 | 57.441 | -57.541 | 35.319 | 0.6554 |
| 71 | DISCARD | lightgbm | 54.320 | 57.518 | -57.618 | 35.170 | 0.6591 |
| 72 | DISCARD | lightgbm | 54.330 | 57.429 | -57.529 | 35.007 | 0.6590 |
| 73 | DISCARD | lightgbm | 54.320 | 57.437 | -57.537 | 34.985 | 0.6591 |
| 74 | DISCARD | lightgbm | 54.581 | 57.502 | -57.602 | 35.254 | 0.6558 |
| 75 | DISCARD | lightgbm | 54.730 | 57.191 | -57.291 | 35.108 | 0.6540 |
| 76 | DISCARD | lightgbm | 54.312 | 57.161 | -57.261 | 35.137 | 0.6592 |
| 77 | DISCARD | catboost | 21.520 | 23.190 | -23.190 | 12.023 | 0.9465 |
| 78 | DISCARD | catboost | 21.058 | 22.472 | -22.472 | 11.496 | 0.9488 |
| 79 | DISCARD | catboost | 21.040 | 22.587 | -22.587 | 11.494 | 0.9489 |
| 80 | DISCARD | catboost | 21.057 | 22.795 | -22.795 | 11.557 | 0.9488 |
| 81 | DISCARD | catboost | 53.929 | 57.857 | -57.957 | 35.235 | 0.6640 |
| 82 | DISCARD | catboost | 53.895 | 58.159 | -58.259 | 35.172 | 0.6644 |
| 83 | DISCARD | catboost | 53.929 | 57.857 | -57.957 | 35.235 | 0.6640 |
| 84 | DISCARD | catboost | 54.155 | 58.075 | -58.175 | 35.348 | 0.6612 |
| 85 | DISCARD | catboost | 53.940 | 57.658 | -57.758 | 35.125 | 0.6639 |
| 86 | DISCARD | catboost | 54.254 | 57.684 | -57.784 | 35.305 | 0.6599 |
| 87 | DISCARD | catboost | 21.188 | 22.476 | -22.476 | 11.442 | 0.9481 |
| 88 | DISCARD | catboost | 20.802 | 22.488 | -22.488 | 11.475 | 0.9500 |
| 89 | DISCARD | catboost | 21.056 | 22.708 | -22.708 | 11.525 | 0.9488 |
| 90 | DISCARD | catboost | 21.133 | 22.467 | -22.467 | 11.500 | 0.9484 |
| 91 | DISCARD | catboost | 21.045 | 22.449 | -22.449 | 11.510 | 0.9488 |
| 92 | DISCARD | catboost | 20.822 | 22.596 | -22.596 | 11.541 | 0.9499 |
| 93 | DISCARD | catboost | 20.945 | 22.569 | -22.569 | 11.531 | 0.9493 |
| 94 | DISCARD | catboost | 21.063 | 22.528 | -22.528 | 11.502 | 0.9487 |
| 95 | DISCARD | catboost | 21.005 | 22.451 | -22.451 | 11.549 | 0.9490 |
| 96 | KEEP | catboost | 20.881 | 22.357 | -22.357 | 11.473 | 0.9496 |
| 97 | KEEP | catboost | 20.735 | 22.167 | -22.167 | 11.398 | 0.9503 |
| 98 | DISCARD | catboost | 20.786 | 22.343 | -22.343 | 11.411 | 0.9501 |
| 99 | DISCARD | catboost | 20.735 | 22.167 | -22.167 | 11.398 | 0.9503 |
| 100 | DISCARD | catboost | 20.726 | 22.178 | -22.178 | 11.348 | 0.9504 |
| 101 | DISCARD | catboost | 20.990 | 22.322 | -22.322 | 11.483 | 0.9491 |
| 102 | DISCARD | catboost | 21.040 | 22.322 | -22.322 | 11.392 | 0.9489 |
| 103 | DISCARD | catboost | 20.820 | 22.352 | -22.352 | 11.440 | 0.9499 |
| 104 | DISCARD | catboost | 20.735 | 22.167 | -22.167 | 11.398 | 0.9503 |

## Champion residual slices (2014 test)

- Onset hours (Δ ≥ 50 µg/m³): n=95 RMSE=103.4 (pred 169 vs actual 248)
- Worst month: 01 RMSE=34.84
- Best month: 07 RMSE=13.13
- Worst hour: 20:00 RMSE=32.48
- Spike F1@75: 0.940 (P=0.930 R=0.951)
- p99 |error|=75.3 · max |error|=499.1
- Skill vs persist-1 **+7.09%** (Exp96 +6.43%, Exp30 +6.15%). JJA 13.84 (no summer tax).
- January still 34.84 vs persist 33.58. January RH>=70 **36.68** vs persist **23.94**. January hour-1 74.63 vs persist 69.40.
- t+6 side ladder unchanged: **Exp76** 54.31/57.16. Do not mix composites.

## Recent notes

- **Exp96 KEEP** dewp_delta. First 1h KEEP since Exp30.
- **Exp97 KEEP** is_heating on Exp96. Val 22.167 test 20.735. January RH bomb only 38.25→36.68. CatBoost 23/50.
- Exp98 heating_night DISCARD (val 22.343). Jan RH>=70 Iws<2 42.65→44.31.
- Exp99 bagging_temperature=2 DISCARD (bit-identical to Exp97). CatBoost 25/50.
- Exp100 rh_iws DISCARD (val 22.178, test 20.726). Jan rh_iws q3 39.39→40.03. CatBoost 26/50.
- Exp101 heating_build DISCARD (val 22.322, test 20.990). Jan persist>=150 delta1>0 53.00→53.86. CatBoost 27/50.
- Exp102 Depthwise DISCARD (val 22.322, test 21.040). High-PRES building-dirty 68.80→77.22. CatBoost 28/50.
- Exp103 pres_delta DISCARD (val 22.352, test 20.820). Onset dPRES>=1 158.68→157.78. CatBoost 29/50.
- Exp104 min_data_in_leaf=20 DISCARD (bit-identical to Exp97). CatBoost 30/50.
