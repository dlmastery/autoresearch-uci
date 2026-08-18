# AutoResearch-UCI

Karpathy-style autonomous research loop on **UCI 381 Beijing PM2.5**.

- **[Live dashboard](dashboard/)** — KEEP ladder, experiment log, reasoning blobs, frozen 2014 split
- **[GitHub repo](https://github.com/dlmastery/autoresearch-uci)**
- Champion: LightGBM Exp30 · **2014 test RMSE 20.945** · skill vs persistence **+6.1%** · 31 experiments / 9 KEEP

## The ladder

```
persistence 22.316
  → Exp1  21.768  KEEP  C&G 2016 XGBoost
  → Exp2  21.996  KEEP  max_depth 4          (val improved)
  → Exp4  22.008  KEEP  lr 0.01
  → Exp8  22.034  KEEP  subsample 0.6
  → Exp14 21.823  KEEP  inversion_spread
  → Exp15 21.290  KEEP  pm25_delta1
  → Exp22 21.122  KEEP  inversion + delta     ← champion
```

Protocol is verbatim from [dlmastery/autoresearch](https://github.com/dlmastery/autoresearch). Grok Build is the outer-loop researcher.
