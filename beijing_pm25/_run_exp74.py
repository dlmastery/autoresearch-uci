"""Exp74 — t+6 bagging_freq=1 on Exp72 extra_trees+linear recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 bagging_freq=1 on Exp72 extra_trees linear (LGB side ladder 48/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--set", "feature_fraction=1.0",
    "--set", "linear_tree=true",
    "--set", "bagging_freq=1",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp72 residuals on moist dirty onsets, not "
        "last fire's February histogram blob. Exp72 extra_trees plus linear_tree test 54.330 "
        "val 57.429, gap 3.10. January 81.14 versus JJA 36.14. Hour 20 63.17. Onset n=991 "
        "RMSE 91.58. New: inversion_spread<=6 and persist>=150 onsets n=129 RMSE 110.39 LOSE "
        "to persist-6 98.51, need +91.0, pred -7.4. The same cell's collapses skill +28.7 "
        "percent. bagging_fraction is 0.6 but bagging_freq is still 0 so every 2010-2012 "
        "moist-haze hour trains every linear leaf. max_bin 127 did not fix February or this "
        "onset hole. Enabling bagging is the unused switch on this recipe."
    ),
    "--citations",
    (
        "Chen, Tianqi and Guestrin, Carlos 2016 KDD 'XGBoost: A Scalable Tree Boosting System' "
        "(arXiv:1603.02754) — stochastic row subsample reduces tree correlation but only when "
        "the bagging frequency is positive; a fraction without a frequency is inert. Relevance: "
        "Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly Efficient "
        "Gradient Boosting Decision Tree' (arXiv:1706.08359) use the same bagging_freq switch. "
        "Exp72 moist persist>=150 onsets still predict -7.4 versus needed +91.0 on the frozen "
        "2014 t+6 timestamps, and bagging_freq default 0 means extra-trees linear leaves see "
        "every 2010-2012 humid-haze hour. bagging_freq=1 is one change from Exp72, not the "
        "discarded greedy Exp61 bagging test."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting bagging_freq from 0 to 1 on the Exp72 t+6 LightGBM "
        "(extra_trees plus linear_tree plus feature_fraction 1.0 plus num_leaves 31 plus "
        "month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW), leaving features "
        "unchanged, will cut 2013 t+6 val RMSE because the mechanism is actual 0.6 row "
        "bagging so extra-trees linear slopes cannot reuse the same 2010-2012 moist-haze "
        "onset hours. Per Chen and Guestrin 2016 that is stochastic bagging. Because max_bin "
        "127 and greedy bagging_freq=1 already failed, this is enabling dormant bagging on "
        "the extra-trees-plus-linear recipe not another histogram. The 1h composite will "
        "DISCARD; the side-ladder KEEP is t+6 val below 57.429. This single change starts "
        "from the current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.6 to 55.8 versus Exp72 54.33, val 56.4 to 58.5, and 1h-gate "
        "composite -61 to -53 (DISCARD). Moist persist>=150 onset increment may move from -7.4 "
        "toward +5 to +40 versus need +91.0. A val RMSE above 58.0 is a side-ladder miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
