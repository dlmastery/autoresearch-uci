"""Exp72 — t+6 linear_tree on Exp70 extra_trees recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 linear_tree=True on Exp70 extra_trees (LGB side ladder 46/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=31",
    "--set", "extra_trees=true",
    "--set", "feature_fraction=1.0",
    "--set", "linear_tree=true",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp70 residuals on typical dirty persist "
        "slopes, not last fire's high-PRES dummy. Exp70 extra_trees plus feature_fraction 1.0 "
        "test 54.620 val 57.441, gap 2.82. January 83.32 versus JJA 36.10. Hour 20 62.90. "
        "Onset n=991 RMSE 91.85. New: on typical persist>=150 n=731, predicted increment "
        "correlates -0.445 with persist while actual increment correlates -0.024. Hours with "
        "|need|<20 and persist>=150 n=302 RMSE 50.16 versus persist-6 11.03, pred -21.4 versus "
        "need -0.3. Constant extra-trees leaves assign a collapse-tilted mean that grows more "
        "negative as persist rises. anticyclone did not change that leaf value. Piece-wise "
        "linear leaves can fit increment near zero along persist."
    ),
    "--citations",
    (
        "Shi, Yu; Li, Jian and Li, Zhize 2018 arXiv 'Gradient Boosting With Piece-Wise Linear "
        "Regression Trees' (arXiv:1802.05640) — each leaf holds a linear model so the booster "
        "can follow a continuous persist slope instead of a constant mean. Relevance: Ke, Meng, "
        "Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient "
        "Boosting Decision Tree' (arXiv:1706.08359) ship this as linear_tree. Exp70 typical "
        "persist>=150 increment correlates -0.445 with persist while the actual 6h change "
        "correlates -0.024 on the frozen 2014 t+6 timestamps, which is exactly the constant-leaf "
        "mean-reversion Shi replace. This is not the discarded 1h greedy Exp37 linear_tree run."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting linear_tree from False to True on the Exp70 t+6 LightGBM "
        "(extra_trees plus feature_fraction 1.0 plus num_leaves 31 plus month_sin plus "
        "pres_delta plus dewp_delta plus cbwd_prev_NW), leaving features unchanged, will cut "
        "2013 t+6 val RMSE because the mechanism is a linear persist slope inside each "
        "extra-trees leaf so typical dirty increment can stay near zero instead of the -24 "
        "collapse mean. Per Shi et al. 2018 that is piece-wise linear leaves. Because "
        "anticyclone and min_data=50 already failed, this is leaf architecture on extra_trees "
        "not another dummy or n_min. The 1h composite will DISCARD; the side-ladder KEEP is "
        "t+6 val below 57.441. This single change starts from the current t+6 recipe on the "
        "frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.4 to 56.5 versus Exp70 54.62, val 56.2 to 59.0, and 1h-gate "
        "composite -62 to -53 (DISCARD). Typical persist>=150 increment may move from -24.2 "
        "toward -14 to +2 versus need -0.7. A val RMSE above 58.2 is a side-ladder miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
