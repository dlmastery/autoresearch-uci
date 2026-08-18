"""Exp69 — t+6 min_data_in_leaf=50 on Exp68 extra_trees recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 min_data_in_leaf=50 on Exp68 extra_trees (LGB side ladder 43/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--set", "min_data_in_leaf=50",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp68 residuals by calendar month, not last "
        "fire's SE-night blob. Exp68 extra_trees test 54.482 val 57.498, gap 3.02. January "
        "82.95 versus JJA 36.22. Hour 20 62.74. Onset n=991 RMSE 91.64. New: February skill "
        "versus persist-6 is -0.3 percent (RMSE 76.41 versus 76.21) with predicted increment "
        "-14.5 versus need 0.0. February typical persist>=150 n=144 RMSE 85.38 versus persist-6 "
        "28.24, need +4.4, pred -40.3, skill -202 percent. Extra-trees paid 2013 val and "
        "January but over-cleans stable February haze through 20-row randomized persist leaves. "
        "Geurts n_min is the unused leaf floor on this extra_trees recipe."
    ),
    "--citations",
    (
        "Geurts, Pierre; Ernst, Damien and Wehenkel, Louis 2006 Machine Learning 'Extremely "
        "randomized trees' — extra-trees need a larger n_min than greedy trees because random "
        "thresholds already add variance, so small leaves overfit noise. Relevance: Ke, Meng, "
        "Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient "
        "Boosting Decision Tree' (arXiv:1706.08359) expose that floor as min_data_in_leaf. Exp68 "
        "ships the default 20 rows per leaf and now loses to persist-6 in February (pred -40.3 "
        "on typical persist>=150 versus need +4.4). Raising the floor to 50 is one change from "
        "Exp68 on the frozen 2014 t+6 timestamps, not the discarded 1h min_data=100 run and not "
        "turning extra_trees off."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting min_data_in_leaf from 20 to 50 on the Exp68 t+6 LightGBM "
        "(extra_trees plus num_leaves 31 plus month_sin plus pres_delta plus dewp_delta plus "
        "cbwd_prev_NW), leaving features unchanged, will cut 2013 t+6 val RMSE because the "
        "mechanism is a larger extra-trees leaf so randomized persist cuts cannot isolate "
        "20-row 2010-2012 February collapse shards. Per Geurts et al. 2006 that is n_min. "
        "Because extra_trees just KEEPed and 1h min_data=100 was a different greedy 63-leaf "
        "nowcast, this is the extra-trees leaf floor not another booster. The 1h composite "
        "will DISCARD; the side-ladder KEEP is t+6 val below 57.498. This single change starts "
        "from the current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.6 to 55.8 versus Exp68 54.48, val 56.4 to 58.4, and 1h-gate "
        "composite -61 to -53 (DISCARD). February typical persist>=150 increment may move from "
        "-40.3 toward -25 to -5 versus need +4.4. A val RMSE above 58.0 is a side-ladder miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
