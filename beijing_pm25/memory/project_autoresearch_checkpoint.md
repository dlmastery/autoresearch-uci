# Autoresearch checkpoint — Beijing PM2.5 (calendar protocol)

**Updated:** 2026-08-18 after Exp1 on frozen 2014
**Composite fingerprint:** still `rmse|false|0.1|-40`
**Split protocol:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- exp 1 · xgboost · composite **−23.354**
- 2013 val RMSE **23.354** · 2014 test RMSE **21.768** · n_test **7950**
- 2014 persistence RMSE **22.316** · skill **+0.025**

## RULE_CHANGE
Old 65/15/20 Exp1 (test RMSE 20.49) is INVALID. Quarantined.

## Next experiment
t+6 on the same frozen 2014 timestamps. Do not change test_hash.

## History
| exp | protocol | test RMSE | vs pers | decision |
|-----|----------|-----------|---------|----------|
| 1 | calendar 2014 | 21.768 | +2.5% | KEEP |
