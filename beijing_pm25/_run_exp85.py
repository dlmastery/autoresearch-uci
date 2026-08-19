"""Exp85 — CatBoost Ordered t+6 on Exp81 Plain recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Ordered t+6 on Exp81 features (CatBoost cycle 11/50)",
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
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp81 t+6 residuals on wrong-sign onsets, "
        "not last fire's RH-tail blob. Exp81 val 57.857 lost to Exp76 57.161, test 53.929 "
        "beat 54.312, val-test gap 3.93 versus LightGBM 2.85. New: need>50 and pred<0 "
        "n=164 RMSE 129.01 versus persist-6 100.47, persist mean 204, need +91.5, pred "
        "-24.9. Exp76 has 189 such hours with pred -25.1. 1h Ordered closed because lag-1 "
        "nowcast shrank; t+6 persist is six hours stale. l2, bagging_temperature, and drop "
        "rh_magnus stay closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — ordered boosting scores each 2010-2012 dirty-rising "
        "hour from a past-only permutation so the leaf cannot learn 'already 204 will drop'. "
        "Relevance: Exp81 still predicts -24.9 versus needed +91.5 on 164 frozen 2014 t+6 "
        "wrong-sign onsets, and Ordered on t+6 is one architecture change from Exp81 Plain, "
        "not the discarded 1h Ordered nowcast or another t+6 leaf-L2."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting boosting_type from Plain to Ordered on the Exp81 "
        "CatBoost t+6 recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, iterations 2000, "
        "month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW plus rh_magnus) will "
        "cut 2013 t+6 val RMSE because the mechanism is past-only leaf values so already-dirty "
        "2010-2012 hours cannot leak a -25 collapse slope onto 2013 onsets. Per Prokhorenkova "
        "et al. 2018 that is ordered boosting. Because 1h Ordered failed on lag-1 and three "
        "Plain t+6 tweaks already missed val, this is a horizon-specific architecture rethink "
        "not another nearby HP. The 1h composite will DISCARD; the side-ladder KEEP is t+6 "
        "val below 57.161. This single change starts from the current t+6 recipe on the "
        "frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.4 to 57.5 versus Exp81 53.93, val 56.4 to 59.5, and "
        "1h-gate composite -61 to -53 (DISCARD). Wrong-sign onset increment may move from "
        "-24.9 toward -10 to +15 versus need +91.5. A val RMSE above 58.5 is a side-ladder "
        "miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
