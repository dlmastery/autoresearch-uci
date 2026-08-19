"""Exp76 — t+6 linear_lambda=1 on Exp75 extra_trees+linear+rh_magnus recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 linear_lambda=1 on Exp75 extra_trees linear rh_magnus (LGB side ladder 50/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--add-feature", "rh_magnus",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--set", "feature_fraction=1.0",
    "--set", "linear_tree=true",
    "--set", "linear_lambda=1",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp75 residuals on the hour-6 blow-up, not "
        "last step's RH 70-85 band. Exp75 rh_magnus side-KEEP val 57.191 test 54.730, gap "
        "2.46. January 80.43 versus JJA 36.10. Hour 23 63.98, hour 22 63.77. Onset n=991 "
        "RMSE 91.06. New: hour 6 RMSE 67.07 versus Exp72 52.76, one RH=100 persist=240 row "
        "predicts 872 versus actual 116 (Exp72 predicted 119.5). persist>=250 typical still "
        "pred -52.2 versus need -0.1. linear_lambda default 0 lets extra-trees linear leaves "
        "extrapolate saturated RH. Bagging and max_bin stay closed."
    ),
    "--citations",
    (
        "Shi, Yu; Li, Jian and Li, Zhize 2018 arXiv 'Gradient Boosting With Piece-Wise "
        "Linear Regression Trees' (arXiv:1802.05640) — each leaf fits a linear model and "
        "an L2 penalty on those coefficients (LightGBM linear_lambda) stops a single "
        "saturated-RH shard from extrapolating persist. Relevance: Exp75's hour-6 RH=100 "
        "row still predicts 872 versus 116 on the frozen 2014 t+6 timestamps after Magnus "
        "RH was added, and linear_lambda=1 is one change from Exp75, not another moisture "
        "formula or the discarded bagging_freq switch."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting linear_lambda from 0 to 1 on the Exp75 t+6 LightGBM "
        "(extra_trees plus linear_tree plus feature_fraction 1.0 plus num_leaves 31 plus "
        "month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW plus rh_magnus), "
        "leaving features unchanged, will cut 2013 t+6 val RMSE because the mechanism is "
        "L2 shrinkage of linear leaf slopes so a saturated-RH extra-trees shard cannot "
        "emit an 872 prediction. Per Shi et al. 2018 that is linear_lambda. Because "
        "rh_magnus just side-KEPT and bagging is closed, this is the unused linear-tree "
        "regularizer not another humidity feature. The 1h composite will DISCARD; the "
        "side-ladder KEEP is t+6 val below 57.191. This single change starts from the "
        "current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.5 to 55.6 versus Exp75 54.73, val 56.3 to 58.2, and "
        "1h-gate composite -61 to -53 (DISCARD). Hour-6 RMSE may move from 67.07 toward "
        "52 to 60, and the RH=100 blow-up pred from 872 toward 100 to 250 versus actual "
        "116. A val RMSE above 57.8 is a side-ladder miss. Ranges are ug/m3 on the "
        "frozen 2014 timestamps."
    ),
])
