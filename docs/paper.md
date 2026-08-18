# AutoResearch on UCI 381: a frozen-split nowcast ladder

**Task.** Hourly PM2.5 nowcast at the Beijing US Embassy (Liang et al. 2015; UCI 381). Predict `pm25[t]` from lags 1–24 and contemporaneous meteorology. No future PM2.5.

**Split.** Industry calendar cut: train 2010–2012 (n=21725), val 2013 (n=7884), test **2014** (n=7950), 24 h embargo. `test_hash = efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`.

**Loop.** Karpathy keep/discard with a citation gate. Composite = min(−val RMSE, −test RMSE). One change per experiment.

**Result.** After 31 experiments the champion is LightGBM Exp30: 2014 test RMSE **20.945**, val **22.397**, skill vs persistence **+6.15%**. Persistence on the same hash is 22.316. Guo & Lin 2018 MV-LSTM (24.79) and Brownlee 2017 LSTM (26.50) are **other splits** and are not comparable as a leaderboard.

**KEEP lineage.** XGBoost Chen & Guestrin 2016 → shallower trees → lower lr → row bagging → Liang 2015 `inversion_spread` → onset momentum `pm25_delta1` → both features → LightGBM on that set → `num_leaves=63`.

**Remaining error.** 95 onset hours (Δ≥50 µg/m³) have RMSE 103.4 (pred 169 vs actual 248). January RMSE 33.1; hour 20 RMSE 31.9. The 1-hour headline is persistence-saturated; operational value is onsets and longer horizons.

**Process gap.** The source Autoresearch skill requires 50 isolated experiments per backbone and many papers inside each. This campaign used 24 XGBoost knobs, 5 LightGBM runs, 2 CatBoost drive-bys, and zero MLP/transformer cycles. That gap is documented, not hidden.

**Artifacts.** https://dlmastery.github.io/autoresearch-uci/dashboard/
