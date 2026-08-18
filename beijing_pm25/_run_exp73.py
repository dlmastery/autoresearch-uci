"""Exp73 — t+6 max_bin=127 on Exp72 extra_trees+linear recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 max_bin=127 on Exp72 extra_trees linear (LGB side ladder 47/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--set", "feature_fraction=1.0",
    "--set", "linear_tree=true",
    "--set", "max_bin=127",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp72 residuals on February, not last fire's "
        "typical-dirty persist-slope blob. Exp72 extra_trees plus linear_tree test 54.330 val "
        "57.429, gap 3.10. January 81.14 versus JJA 36.14. Hour 20 63.17. Onset n=991 RMSE "
        "91.58. New: February skill versus persist-6 is -2.9 percent (RMSE 78.42 versus 76.21), "
        "worse than Exp68 -0.3 percent, with predicted increment -16.4 versus need 0.0. February "
        "typical persist>=150 n=144 RMSE 81.89 versus persist-6 28.24, need +4.4, pred -41.1. "
        "Linear extra-trees paid January and 2013 val by over-cleaning February through 255-bin "
        "random persist thresholds. Coarser max_bin is the unused Ke histogram floor on this recipe."
    ),
    "--citations",
    (
        "Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly Efficient "
        "Gradient Boosting Decision Tree' (arXiv:1706.08359) — max_bin sets the histogram "
        "granularity of every split; fewer bins reduce extra-trees threshold noise. Relevance: "
        "Shi, Yu; Li, Jian and Li, Zhize 2018 arXiv 'Gradient Boosting With Piece-Wise Linear "
        "Regression Trees' (arXiv:1802.05640) fit a linear model on those bins, so 255 random "
        "persist cuts let February collapse shards set a steep negative slope. Exp72 February "
        "typical persist>=150 still predicts -41.1 versus needed +4.4 on the frozen 2014 t+6 "
        "timestamps. Cutting max_bin to 127 is one change from Exp72, not the discarded 1h "
        "greedy max_bin=127 run."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting max_bin from 255 to 127 on the Exp72 t+6 LightGBM "
        "(extra_trees plus linear_tree plus feature_fraction 1.0 plus num_leaves 31 plus "
        "month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW), leaving features "
        "unchanged, will cut 2013 t+6 val RMSE because the mechanism is coarser persist "
        "histograms so extra-trees linear slopes cannot isolate 2010-2012 February collapse "
        "shards. Per Ke et al. 2017 that is max_bin. Because linear_tree just KEEPed and 1h "
        "max_bin=127 was greedy nowcast, this is the extra-trees-plus-linear histogram floor "
        "not another leaf architecture. The 1h composite will DISCARD; the side-ladder KEEP "
        "is t+6 val below 57.429. This single change starts from the current t+6 recipe on "
        "the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.6 to 55.8 versus Exp72 54.33, val 56.4 to 58.4, and 1h-gate "
        "composite -61 to -53 (DISCARD). February typical persist>=150 increment may move from "
        "-41.1 toward -28 to -8 versus need +4.4. A val RMSE above 58.0 is a side-ladder miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
