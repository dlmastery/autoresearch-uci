"""Exp71 — t+6 add anticyclone PRES>=1020 on Exp70 extra_trees recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 add anticyclone PRES>=1020 on Exp70 extra_trees (LGB side ladder 45/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--add-feature", "anticyclone",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--set", "feature_fraction=1.0",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp70 residuals on high-pressure dirty air, "
        "not last fire's Saturday column-dropout blob. Exp70 extra_trees plus feature_fraction "
        "1.0 test 54.620 val 57.441, gap 2.82. January 83.32 versus JJA 36.10. Hour 20 62.90. "
        "Onset n=991 RMSE 91.85. New: persist>=150 under PRES>=1022 n=535 RMSE 98.77 holds 22 "
        "percent of SSE, need -25.6, pred -53.9. Extra-trees over-cleans trapped high-pressure "
        "haze. October persist>=150 is already calibrated (-15.6 versus -15.3). feature_fraction "
        "1.0 did not stop the high-PRES mean-reversion. PRES is already a column; a binary "
        "anticyclone names the synoptic trap that random PRES thresholds smear."
    ),
    "--citations",
    (
        "Liang, Zou, Guo, Li, Zhang, Zhang, Huang and Chen 2015 Proceedings of the Royal "
        "Society A 'Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and "
        "winter heating' — high surface pressure with weak winds is the documented Beijing "
        "haze trap, so a PRES>=1020 dummy is the unused synoptic split, not another pressure "
        "tendency. Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A "
        "Highly Efficient Gradient Boosting Decision Tree' (arXiv:1706.08359) — one extra "
        "binary is a cheap extra-trees split. Relevance: Exp70 still predicts -53.9 on "
        "high-PRES persist>=150 hours versus needed -25.6 on the frozen 2014 t+6 timestamps, "
        "and pres_delta already KEEPed the tendency channel."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding anticyclone, a valid issue-time binary that is one when "
        "PRES is at least 1020 hPa, to the Exp70 t+6 LightGBM (extra_trees plus feature_fraction "
        "1.0 plus num_leaves 31 plus month_sin plus pres_delta plus dewp_delta plus "
        "cbwd_prev_NW), leaving every booster knob unchanged, will cut 2013 t+6 val RMSE "
        "because the mechanism is one extra-trees split on the high-pressure trap that random "
        "PRES thresholds smear into persist mean-reversion. Per Liang et al. 2015 that "
        "anticyclone is the haze cage. Because pres_delta already paid and Saturday ff=1.0 "
        "did not fix high-PRES over-clean, this is a synoptic dummy not another tendency or "
        "column fraction. The 1h composite will DISCARD; the side-ladder KEEP is t+6 val "
        "below 57.441. This single change starts from the current t+6 recipe on the frozen "
        "2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.6 to 55.8 versus Exp70 54.62, val 56.4 to 58.4, and 1h-gate "
        "composite -61 to -53 (DISCARD). High-PRES persist>=150 increment may move from -53.9 "
        "toward -40 to -20 versus need -25.6. A val RMSE above 58.0 is a side-ladder miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
