"""Exp70 — t+6 feature_fraction 1.0 on Exp68 extra_trees recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 feature_fraction 1.0 on Exp68 extra_trees (LGB side ladder 44/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--set", "feature_fraction=1.0",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp68 residuals on weekend and calm-dirty "
        "onsets, not last fire's February n_min blob. Exp68 extra_trees test 54.482 val "
        "57.498, gap 3.02. January 82.95 versus JJA 36.22. Hour 20 62.74. Onset n=991 RMSE "
        "91.64. New: Saturday persist>=100 n=485 RMSE 87.16 versus persist-6 88.33, skill "
        "only +1.3 percent, while Sunday persist>=100 skill is +15.8 percent. cv persist>=150 "
        "onsets n=111 RMSE 111.87 LOSE to persist-6 101.19, need +92.7 pred -1.3. Extra-trees "
        "already randomizes thresholds; feature_fraction 0.8 can drop Iws, dow, or SE on the "
        "trees that need them. min_data=50 did not fix the weekend hole."
    ),
    "--citations",
    (
        "Geurts, Pierre; Ernst, Damien and Wehenkel, Louis 2006 Machine Learning 'Extremely "
        "randomized trees' — extra-trees get their variance reduction from random split "
        "thresholds, not from column dropout, so feature_fraction can stay 1.0. Relevance: "
        "Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly "
        "Efficient Gradient Boosting Decision Tree' (arXiv:1706.08359) expose feature_fraction "
        "as optional column subsample. Exp68 Saturday persist>=100 skill is only +1.3 percent "
        "and calm-dirty onsets predict -1.3 versus needed +92.7, which is consistent with "
        "trees that never saw dow and Iws together. Raising feature_fraction from 0.8 to 1.0 "
        "is one change from Exp68 on the frozen 2014 t+6 timestamps, not the discarded greedy "
        "feature_fraction 0.6 run."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting feature_fraction from 0.8 to 1.0 on the Exp68 t+6 "
        "LightGBM (extra_trees plus num_leaves 31 plus month_sin plus pres_delta plus "
        "dewp_delta plus cbwd_prev_NW), leaving features unchanged, will cut 2013 t+6 val "
        "RMSE because the mechanism is every tree seeing dow, Iws, and SE so extra-trees "
        "random thresholds no longer miss Saturday dirty and calm-dirty onset leaves. Per "
        "Geurts et al. 2006 randomization lives in the threshold, not in dropped columns. "
        "Because min_data=50 and greedy feature_fraction 0.6 already failed, this is turning "
        "off double randomization not another leaf floor. The 1h composite will DISCARD; the "
        "side-ladder KEEP is t+6 val below 57.498. This single change starts from the current "
        "t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.6 to 55.8 versus Exp68 54.48, val 56.4 to 58.4, and 1h-gate "
        "composite -61 to -53 (DISCARD). Saturday persist>=100 skill may move from +1.3 percent "
        "toward +4 to +14. cv persist>=150 onset increment may move from -1.3 toward +10 to +50. "
        "A val RMSE above 58.0 is a side-ladder miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
