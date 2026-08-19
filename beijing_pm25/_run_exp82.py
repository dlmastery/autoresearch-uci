"""Exp82 — CatBoost t+6 l2_leaf_reg 3 to 10 on Exp81 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost t+6 l2_leaf_reg=10 on Exp81 Plain (CatBoost cycle 8/50)",
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
    "--set", "l2_leaf_reg=10",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp81 t+6 residuals on the val gap, not "
        "last step's pre-run Saturday blob. Exp81 CatBoost Plain test 53.929 beat Exp76 "
        "54.312 but val 57.857 lost to 57.161. New: Saturday typical RMSE 36.78 versus "
        "Exp76 39.80 still far from persist-6 24.07, pred +7.1 versus need +3.3. February "
        "71.69 beat Exp76 78.50 and persist 76.21. persist>=250 typical pred -45.7 versus "
        "Exp76 -52.7. 2014 test improved; 2013 val is the side-ladder bottleneck. l2_leaf_reg "
        "is still 3. 1h Ordered/lr/depth stay closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — l2_leaf_reg shrinks oblivious-leaf values and is "
        "the default-3 knob they use to stop a small 2010-2012 Saturday shard from owning "
        "a large increment. Relevance: Exp81 still has t+6 val 57.857 versus Exp76 57.161 "
        "on the frozen calendar split while 2014 test already beat 54.312, so raising "
        "l2_leaf_reg to 10 is one change from Exp81, not another 1h depth or lr."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting l2_leaf_reg from 3 to 10 on the Exp81 CatBoost Plain "
        "t+6 recipe (depth 6, learning_rate 0.03, iterations 2000, month_sin plus pres_delta "
        "plus dewp_delta plus cbwd_prev_NW plus rh_magnus) will cut 2013 t+6 val RMSE because "
        "the mechanism is stronger leaf L2 so 2010-2012 Saturday typical shards cannot keep "
        "a +7 increment that fails to transfer to 2013. Per Prokhorenkova et al. 2018 that "
        "is l2_leaf_reg. Because Exp81 already won 2014 test and 1h regularizers are closed, "
        "this is the unused CatBoost leaf penalty on the new t+6 recipe. The 1h composite "
        "will DISCARD; the side-ladder KEEP is t+6 val below 57.161. This single change "
        "starts from the current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.4 to 56.5 versus Exp81 53.93, val 56.5 to 59.0, and "
        "1h-gate composite -60 to -53 (DISCARD). Saturday typical RMSE may move from 36.78 "
        "toward 28 to 36 versus persist-6 24.07. A val RMSE above 58.2 is a side-ladder "
        "miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
