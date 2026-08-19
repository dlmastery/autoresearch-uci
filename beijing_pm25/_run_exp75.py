"""Exp75 — t+6 add rh_magnus Magnus RH on Exp72 extra_trees+linear recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 add rh_magnus Magnus RH on Exp72 extra_trees linear (LGB side ladder 49/50)",
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
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp72 residuals on RH-band and extreme-persist "
        "typical hours, not last fire's moist-onset bagging blob. Exp72 extra_trees plus "
        "linear_tree test 54.330 val 57.429, gap 3.10. January 81.14 versus JJA 36.14. Hour 22 "
        "is now worst at 65.19 (hour 20 63.17). Onset n=991 RMSE 91.58. New: persist>=250 "
        "typical n=237 RMSE 82.39 versus persist-6 28.27, skill -191.5 percent, need -0.1, "
        "pred -51.5. RH 70-85 persist>=150 n=426 skill only +4.8 percent, those onsets pred "
        "+6.9 versus need +81.1. inversion_spread already in the recipe cannot isolate that "
        "RH band because Magnus RH is nonlinear in TEMP and DEWP. Bagging and max_bin closed."
    ),
    "--citations",
    (
        "Tie, Xuexi; Huang, Ru-Jin; Cao, Junji; Zhang, Qiang; Cheng, Yafang; Su, Hang; "
        "Chang, Di; Poeschl, Ulrich; Hoffmann, Thorsten; Dusek, Ulrike; Li, Guohui; "
        "Worsnop, Douglas R. and O'Dowd, Colin D. 2017 Nature Scientific Reports "
        "'Severe Pollution in China Amplified by Atmospheric Moisture' "
        "(doi:10.1038/s41598-017-11457-w) — aerosol water at high relative humidity "
        "accelerates secondary PM2.5, so the nonlinear Magnus RH from TEMP and DEWP is "
        "the moisture state inversion_spread smears across winter versus summer "
        "temperatures. Relevance: Exp72 RH 70-85 persist>=150 hours still skill only "
        "+4.8 percent on the frozen 2014 t+6 timestamps, and adding rh_magnus is one "
        "change from Exp72, not another extra-trees regularizer after bagging_freq=1 "
        "discarded."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding rh_magnus, the Magnus-Tetens relative humidity "
        "computed from as-of-t-6 TEMP and DEWP, to the Exp72 t+6 LightGBM (extra_trees "
        "plus linear_tree plus feature_fraction 1.0 plus num_leaves 31 plus month_sin "
        "plus pres_delta plus dewp_delta plus cbwd_prev_NW), leaving every booster knob "
        "unchanged, will cut 2013 t+6 val RMSE because the mechanism is one leaf-wise "
        "split on the RH 70-85 band that inversion_spread cannot isolate at cold versus "
        "warm temperatures. Per Tie et al. 2017 that moisture state amplifies secondary "
        "PM. Because bagging_freq=1 and max_bin 127 already failed, this is the unused "
        "nonlinear humidity feature not another histogram. The 1h composite will DISCARD; "
        "the side-ladder KEEP is t+6 val below 57.429. This single change starts from "
        "the current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.6 to 55.8 versus Exp72 54.33, val 56.4 to 58.4, and "
        "1h-gate composite -61 to -53 (DISCARD). RH 70-85 persist>=150 onset increment "
        "may move from +6.9 toward +15 to +45 versus need +81.1. Persist>=250 typical "
        "increment may move from -51.5 toward -40 to -15 versus need -0.1. A val RMSE "
        "above 58.0 is a side-ladder miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
