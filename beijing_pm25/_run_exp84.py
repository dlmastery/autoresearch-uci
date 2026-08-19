"""Exp84 — CatBoost t+6 drop rh_magnus from Exp81 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost t+6 drop rh_magnus from Exp81 Plain (CatBoost cycle 10/50)",
    "--backbone", "catboost",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--add-feature", "rh_magnus",
    "--drop-feature", "rh_magnus",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp83 as a no-op: bagging_temperature=2 "
        "matched Exp81 bit for bit, so the January and RH-tail hole is not Bayesian "
        "temperature. Exp81 January 82.18 versus Exp76 80.40. RH<40 47.28 versus 46.72. "
        "RH>=85 56.25 versus 55.53. RH 40-70 is the only CatBoost win. Oblivious trees "
        "use rh_magnus to lock mid-RH shards and miss both tails. inversion_spread is "
        "already in the recipe. l2=10 and bagging_temperature stay closed."
    ),
    "--citations",
    (
        "Tie, Xuexi; Huang, Ru-Jin; Cao, Junji; Zhang, Qiang; Cheng, Yafang; Su, Hang; "
        "Chang, Di; Poeschl, Ulrich; Hoffmann, Thorsten; Dusek, Ulrike; Li, Guohui; "
        "Worsnop, Douglas R. and O'Dowd, Colin D. 2017 Nature Scientific Reports "
        "'Severe Pollution in China Amplified by Atmospheric Moisture' "
        "(doi:10.1038/s41598-017-11457-w) — relative humidity is a nonlinear moisture "
        "state, but only if the learner can isolate the tails. Relevance: Exp81 CatBoost "
        "Plain still loses both RH<40 and RH>=85 on the frozen 2014 t+6 timestamps while "
        "winning only RH 40-70, so dropping rh_magnus is one change from Exp81, not "
        "another inert bagging_temperature after the bit-identical Exp83."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping rh_magnus from the Exp81 CatBoost Plain t+6 recipe "
        "(depth 6, learning_rate 0.03, l2_leaf_reg 3, iterations 2000, month_sin plus "
        "pres_delta plus dewp_delta plus cbwd_prev_NW) will cut 2013 t+6 val RMSE because "
        "the mechanism is removing the mid-RH lock so oblivious trees fall back to "
        "inversion_spread and DEWP which already mark dry versus saturated air. Per Tie "
        "et al. 2017 moisture still matters, but CatBoost cannot use Magnus RH the way "
        "Exp76 linear_tree did. Because bagging_temperature=2 was inert, this is a feature "
        "rethink not another bootstrap HP. The 1h composite will DISCARD; the side-ladder "
        "KEEP is t+6 val below 57.161. This single change starts from the current t+6 "
        "recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.5 to 56.8 versus Exp81 53.93, val 56.4 to 59.0, and "
        "1h-gate composite -60 to -53 (DISCARD). RH<40 RMSE may move from 47.28 toward "
        "45.5 to 47.0 versus Exp76 46.72. A val RMSE above 58.2 is a side-ladder miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
