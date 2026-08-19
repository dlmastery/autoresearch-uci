"""Exp83 — CatBoost t+6 bagging_temperature 1 to 2 on Exp81 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost t+6 bagging_temperature=2 on Exp81 Plain (CatBoost cycle 9/50)",
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
    "--set", "boosting_type=Plain",
    "--set", "bagging_temperature=2",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp81 residuals on January and RH tails, "
        "not last fire's Saturday typical blob. Exp81 test 53.929 beat Exp76 54.312 but "
        "val 57.857 lost to 57.161. New: January RMSE 82.18 versus Exp76 80.40. RH<40 "
        "n=2907 RMSE 47.28 versus 46.72. RH>=85 n=973 RMSE 56.25 versus 55.53. RH 40-70 "
        "is the only band CatBoost wins (56.00 versus 57.44). bagging_temperature is still "
        "1. l2=10 already failed val. Ordered stays closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — bagging_temperature is the Bayesian-bootstrap "
        "temperature that reweights each 2010-2012 hour so a mid-RH shard cannot dominate "
        "every oblivious tree. Relevance: Exp81 still loses January and both RH tails on "
        "the frozen 2014 t+6 timestamps while winning only RH 40-70, and raising "
        "bagging_temperature from 1 to 2 is one change from Exp81, not the discarded l2=10 "
        "leaf penalty."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting bagging_temperature from 1 to 2 on the Exp81 CatBoost "
        "Plain t+6 recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, iterations 2000, "
        "month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW plus rh_magnus) will "
        "cut 2013 t+6 val RMSE because the mechanism is hotter Bayesian bootstrap so "
        "mid-RH 2010-2012 hours cannot own every symmetric split. Per Prokhorenkova et al. "
        "2018 that is bagging_temperature. Because l2=10 already failed val, this is the "
        "unused bootstrap knob not another leaf penalty. The 1h composite will DISCARD; "
        "the side-ladder KEEP is t+6 val below 57.161. This single change starts from the "
        "current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.4 to 56.8 versus Exp81 53.93, val 56.5 to 59.0, and "
        "1h-gate composite -60 to -53 (DISCARD). January RMSE may move from 82.18 toward "
        "78 to 81 versus Exp76 80.40. A val RMSE above 58.2 is a side-ladder miss. Ranges "
        "are ug/m3 on the frozen 2014 timestamps."
    ),
])
