"""Exp67 — t+6 num_leaves 31 to 15 on Exp59 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 num_leaves 31 to 15 on Exp59 recipe (LGB side ladder 41/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=15",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp59 residuals on typical hours versus "
        "persist-6, not last fire's L1 leaf-penalty blob. Exp59 test 54.419 val 57.601, "
        "gap 3.18. January 83.79 versus JJA 36.27. Hour 20 63.42. Onset n=991 RMSE 92.17. "
        "New: on the 5941 typical hours with |actual-persist|<=50 the model RMSE 29.28 LOSES "
        "to persist-6 23.36 (skill -25.3 percent) while overall skill is only a tail salvage. "
        "Typical persist>=150 n=731 RMSE 54.25 versus persist-6 28.31, need -0.7, pred -20.4. "
        "February typical n=414 RMSE 45.86 versus persist-6 23.54. Leaf L1/L2 just failed to "
        "move wrong-sign onsets. 31 leaves still carve high-persist collapse shards that pull "
        "stable dirty hours to -20. The unused capacity cut is num_leaves 15, not another penalty."
    ),
    "--citations",
    (
        "Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly Efficient "
        "Gradient Boosting Decision Tree' (arXiv:1706.08359) — leaf-wise growth overfits small "
        "groups unless num_leaves is capped; they treat 31 as the starting regularizer and say "
        "to lower it when residuals are noisy. Relevance: Exp59 typical persist>=150 hours still "
        "predict -20.4 versus needed -0.7 because 31 leaves isolate 2010-2012 collapse shards "
        "that do not repeat as a 6h drop in 2013-2014, and Exp66 L1 did not shrink those leaves. "
        "Cutting to 15 is one capacity change from Exp59 on the frozen 2014 t+6 timestamps, not "
        "another L1/L2 coefficient."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting num_leaves from 31 to 15 on the Exp59 t+6 LightGBM "
        "(month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW), leaving features "
        "unchanged, will cut 2013 t+6 val RMSE because the mechanism is fewer leaf-wise "
        "partitions so high-persist collapse shards cannot pull typical dirty hours to a -20 "
        "increment. Per Ke et al. 2017 lowering num_leaves is the leaf-wise regularizer when "
        "data are noisy. Because reg_alpha and reg_lambda already failed, this is capacity not "
        "another leaf penalty. The 1h composite will DISCARD; the side-ladder KEEP is t+6 val "
        "below 57.601. This single change starts from the current t+6 recipe on the frozen 2014 "
        "test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.6 to 56.2 versus Exp59 54.42, val 56.4 to 58.8, and 1h-gate "
        "composite -62 to -53 (DISCARD). Typical persist>=150 predicted increment may move from "
        "-20.4 toward -14 to -2 versus need -0.7. A val RMSE above 58.2 is a side-ladder miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
