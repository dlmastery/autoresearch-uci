## Experiment Log — XGBoost Phase (frozen calendar protocol)

### RULE_CHANGE
Fractional 65/15/20 results are quarantined in `_quarantined_fractional_651520/`. Test set is now calendar year **2014**.

### Exp1: baseline XGBoost 1-hour nowcast
- **Config delta from champion:** first run on the frozen protocol (Chen & Guestrin 2016 defaults)
- **Rationale:** industry calendar-year holdout; trees should split on ventilation collapse
- **Prediction:** 2014 test RMSE 20 to 35; skill vs persistence 0.02 to 0.12
- **Result:** Composite −23.354 | Test RMSE 21.768 | Val RMSE 23.354 | n_test=7950
- **2014 persistence:** RMSE 22.316 | MAE 12.035 | skill +0.025
- **Status:** KEEP
- **Learning:** 1-hour nowcast still persistence-dominated on a real future year. Next try t+6 on the same frozen 2014 timestamps.
