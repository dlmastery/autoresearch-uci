## Experiment Log — XGBoost hill-climb on frozen 2014

Composite = min(−val, −test). KEEP iff composite rises. Test year is frozen.

### KEEP lineage
| Exp | Delta | Test RMSE | Val RMSE | Composite |
|---:|---|---:|---:|---:|
| 1 | C&G 2016 baseline | 21.768 | 23.354 | −23.354 |
| 2 | max_depth 4 | 21.996 | 23.205 | −23.205 |
| 4 | learning_rate 0.01 | 22.008 | 23.124 | −23.124 |
| 8 | subsample 0.6 | 22.034 | 22.983 | −22.983 |
| 14 | inversion_spread | 21.823 | 22.885 | −22.885 |
| 15 | pm25_delta1 | 21.290 | 22.684 | −22.684 |
| **22** | **stack inversion onto delta** | **21.122** | **22.470** | **−22.470** |

### Champion
XGBoost depth 4, lr 0.01, subsample 0.6, features = original + `pm25_delta1` + `inversion_spread`.
2014 persistence RMSE 22.316. Skill **+5.4%** (was +2.5% at Exp1).

### Closed axes (DISCARD)
depth 8/5/3, lr 0.05/0.005, min_child 10/50, gamma 1, colsample 0.5, L1/L2 bumps, more trees, weather lags, raw hour, subsample 1.0/0.5, vanilla LightGBM/CatBoost and the same on delta features (LGB test 20.90 looked good but val 22.71 lost the composite).
