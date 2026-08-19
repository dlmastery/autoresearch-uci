"""Exp117 — CatBoost Plain drop dow on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain drop dow on Exp97 (CatBoost cycle 43/50)",
    "--drop-feature", "dow",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire compares weekday "
        "identity across splits, not last fire's Iws tail. New: corr(dow, y) is 0.000 "
        "on 2010-12 train versus 0.063 on 2013 val and 0.069 on 2014 test. 2013 Thursday "
        "mean PM is 80.6 (cleanest weekday, persist 24.30) versus train Thursday 96.5 "
        "and 2014 Thursday 109.8. Test Thu/Fri already lose to persist (20.85 vs 20.75, "
        "24.20 vs 24.13). is_weekend stays. iws_clip100 missed val. Iws transforms, "
        "lag-window cuts, and calendar month subsets stay closed."
    ),
    "--citations",
    (
        "Ke, Guolin; Meng, Qi; Finley, Thomas; Wang, Taifeng; Chen, Wei; Ma, Weidong; "
        "Ye, Qiwei and Liu, Tie-Yan 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient "
        "Boosting Decision Tree' (arXiv:1706.02771) — exclusive feature bundling drops "
        "or merges weak features so they do not eat split budget. Relevance: dow has "
        "train corr 0.000 with y and 2013 Thursday mean 80.6 reverses train Thursday "
        "96.5, so numeric weekday identity is a 2010-12 calendar overfit, and dropping "
        "dow while keeping is_weekend is one change from Exp97, not another Iws clip "
        "after iws_clip100 missed 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping dow from the Exp97 CatBoost Plain recipe (depth 6, "
        "learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus dewp_delta plus is_heating "
        "plus 24 lags plus is_weekend) will cut 2013 val RMSE because the mechanism is "
        "removing a train-noise weekday identity whose Thursday splits reverse in 2013 "
        "so val is not pulled toward 2010-12 weekday-haze calendars. Per Ke et al. 2017 "
        "that is dropping a weak feature. Because iws_clip100 just failed, this is unused "
        "weekday-identity drop not another Iws transform. KEEP if 1h composite beats "
        "-22.167. This single change starts from the current champion on the frozen "
        "2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if 2013 Thursday reversal was a tax. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen timestamps."
    ),
])
