# Autoresearch checkpoint — after Exp31 (original 7-step process)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM
- composite **−22.397**
- 2014 test RMSE **20.945** · 2013 val RMSE **22.397**
- vs Exp1: test 21.768 → 20.945 · val 23.354 → 22.397
- vs 2014 persistence 22.316: skill **+6.1%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, n_estimators 2000, early_stop 50
- features: base + `pm25_delta1` + `inversion_spread`

## KEEP chain
1 → 2 → 4 → 8 → 14 → 15 → 22 (XGB inversion+delta) → **29 LightGBM same features** → **30 num_leaves 63**

## Last live diagnosis (Exp29 residuals)
January RMSE 32.78 (was 35.38 on XGB). Onset RMSE still **109.6** (83 hours, pred 172 vs actual 259). Hour 20 still 31.6. Val still the bottleneck.

## Exhausted / just tested
Exp31 `is_heating` DISCARD (composite −22.417). Heating is already in TEMP. Do not retry a winter dummy.

## Next (original process)
Onset/collapse is the remaining mechanism (RMSE 110 on jumps). Next changes should target that: longer momentum (`pm25_lag1-pm25_lag3`), or a collapse feature, or t+6. Not another num_leaves value until onset is re-diagnosed.

## History
31 experiments, 9 KEEP, 22 DISCARD. Scheduled 30-minute 7-step continuation is armed.
