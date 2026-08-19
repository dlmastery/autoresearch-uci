"""Exp86 — CatBoost Ordered t+6 random_strength 1 to 2 on Exp85."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Ordered t+6 random_strength=2 on Exp85 (CatBoost cycle 12/50)",
    "--backbone", "catboost",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--add-feature", "rh_magnus",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Ordered",
    "--set", "random_strength=2",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp85 Ordered residuals, not last step's "
        "pre-run wrong-sign count. Exp85 val 57.658 beat Exp81 57.857 but lost to Exp76 "
        "57.161; test 53.940 still beats 54.312. New: wrong-sign onsets on the Exp81 mask "
        "pred -23.1 versus Exp81 -24.9 (need +91.5), n rose 164 to 172. January 83.34 "
        "worse than Exp81 82.18. random_strength is still 1. Plain t+6 tweaks stay closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — random_strength adds Gaussian noise to split scores "
        "so one 2010-2012 already-dirty hour cannot always win the oblivious cut. Relevance: "
        "Exp85 Ordered still predicts -23.1 versus needed +91.5 on the frozen 2014 t+6 "
        "wrong-sign onsets and still loses 2013 val by 0.50, and random_strength=2 is one "
        "change from Exp85, not the inert bagging_temperature no-op."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting random_strength from 1 to 2 on the Exp85 CatBoost "
        "Ordered t+6 recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, iterations 2000, "
        "month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW plus rh_magnus) will "
        "cut 2013 t+6 val RMSE because the mechanism is noisier split scores so Ordered "
        "trees cannot lock the same persist>=204 collapse cut. Per Prokhorenkova et al. "
        "2018 that is random_strength. Because Ordered just moved val 57.86 to 57.66, this "
        "is the unused split-noise knob not another leaf L2. The 1h composite will DISCARD; "
        "the side-ladder KEEP is t+6 val below 57.161. This single change starts from the "
        "current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.4 to 56.5 versus Exp85 53.94, val 56.3 to 58.8, and "
        "1h-gate composite -60 to -53 (DISCARD). Wrong-sign onset increment may move from "
        "-23.1 toward -15 to +5 versus need +91.5. A val RMSE above 58.2 is a side-ladder "
        "miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
