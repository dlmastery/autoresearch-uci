## Exp1 — XGBoost 1-hour nowcast on frozen 2014
**Diagnosis:** RULE_CHANGE to calendar years. No valid prior champion.
**Citations:** Chen & Guestrin 2016 KDD (arXiv:1603.02754); Liang et al. 2015 Proc. Royal Society A; Bergmeir, Hyndman & Koo 2018 IJF (arXiv:1905.11744).
**Hypothesis:** Depth-6 XGBoost beats 2014 persistence via ventilation splits.
**Prediction:** Test RMSE 20.0 to 35.0; skill 0.02 to 0.12.
**Verdict:** KEEP. Test RMSE 21.768 vs persistence 22.316 (skill +2.5%).
**Learning:** Axis open at t+6 / episode onsets. Axis closed for more 1-hour tree HPs and for fractional splits.
