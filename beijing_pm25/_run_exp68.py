"""Exp68 — t+6 extra_trees on Exp59 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 extra_trees=True on Exp59 recipe (LGB side ladder 42/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp59 residuals on southeast-wind collapses, "
        "not last fire's typical-dirty capacity blob. Exp59 test 54.419 val 57.601, gap 3.18. "
        "January 83.79 versus JJA 36.27. Hour 20 63.42. Onset n=991 RMSE 92.17. New: SE "
        "collapses n=271 RMSE 107.24 need -107.1 pred -21.2, while NW collapses predict -70.9 "
        "versus need -121.8. SE-night collapses n=162 RMSE 111.04 need -106.4 pred only -12.9. "
        "SE dirty Iws-down skill is only +5.4 percent. num_leaves 15 left typical persist>=150 "
        "at -20.4 and did not touch this SE-break hole. Greedy persist/SE thresholds look like "
        "the remaining unused architecture, not another leaf count or L1 penalty."
    ),
    "--citations",
    (
        "Geurts, Pierre; Ernst, Damien and Wehenkel, Louis 2006 Machine Learning 'Extremely "
        "randomized trees' — extra-trees draw a random threshold per feature instead of a greedy "
        "loss-minimizing cut, which cuts variance when a few high-loss columns dominate. "
        "Relevance: Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly "
        "Efficient Gradient Boosting Decision Tree' (arXiv:1706.08359) ship extra_trees on the "
        "same leaf-wise booster. Exp59 SE-night collapses still predict -12.9 versus needed "
        "-106.4 because greedy persist splits memorize 2010-2012 SE-break shapes that do not "
        "repeat in 2013, and cutting to 15 leaves did not change that. Random thresholds are "
        "one change from Exp59 on the frozen 2014 t+6 timestamps, not another num_leaves step."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting extra_trees from False to True on the Exp59 t+6 LightGBM "
        "(num_leaves 31 plus month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW), "
        "leaving features unchanged, will cut 2013 t+6 val RMSE because the mechanism is "
        "randomized persist and SE thresholds so 2010-2012 nocturnal SE-break shards cannot "
        "own a greedy leaf. Per Geurts et al. 2006 that is extra-trees variance reduction. "
        "Because num_leaves 15 and reg_alpha already failed, this is split randomization not "
        "another capacity or L1 penalty. The 1h composite will DISCARD; the side-ladder KEEP "
        "is t+6 val below 57.601. This single change starts from the current t+6 recipe on the "
        "frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.8 to 56.5 versus Exp59 54.42, val 56.8 to 59.5, and 1h-gate "
        "composite -62 to -53 (DISCARD). SE-night collapse increment may move from -12.9 toward "
        "-50 to -8 versus need -106.4. A val RMSE above 58.4 is a side-ladder miss. Ranges are "
        "ug/m3 on the frozen 2014 timestamps."
    ),
])
