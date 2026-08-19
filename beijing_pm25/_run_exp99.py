"""Exp99 — CatBoost Plain bagging_temperature=2 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain bagging_temperature=2 on Exp97 (CatBoost cycle 25/50)",
    "--set", "bagging_temperature=2",
    "--diagnosis",
    (
        "1h champion remains Exp97: test 20.735, val 22.167 so val is the bottleneck, "
        "January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, onset n=83 "
        "RMSE 110.06 losing to persist-1 107.80. This fire recomputes Exp98 residuals, "
        "not the pre-run nocturnal blob. Exp98 DISCARD val 22.343. New: January RH>=70 "
        "hours 0-5 only 38.33 to 37.60 versus persist 18.85. January RH>=70 Iws<2 worsened "
        "42.65 to 44.31 versus persist 22.94. heating_night is redundant with is_heating "
        "plus hour_sin. bagging_temperature is still 1 on 1h Plain. t+6 T=2 was inert on "
        "a different feature set. heating_night stays closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — bagging_temperature is the Bayesian-bootstrap "
        "temperature that reweights 2010-2012 hours so a January moist-calm shard cannot "
        "own every oblivious tree. Relevance: Exp98 still RMSE 44.31 versus persist-1 "
        "22.94 on January RH>=70 Iws<2 hours on the frozen 2014 nowcast, and "
        "bagging_temperature=2 is one change from Exp97, not another clock product after "
        "heating_night taxed val."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting bagging_temperature from 1 to 2 on the Exp97 CatBoost "
        "Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus "
        "dewp_delta plus is_heating, no heating_night) will cut 2013 val RMSE because "
        "the mechanism is hotter Bayesian bootstrap so January moist-calm 2010-2012 hours "
        "cannot own every symmetric split that over-cleans. Per Prokhorenkova et al. 2018 "
        "that is bagging_temperature. Because heating_night just failed, this is the "
        "unused 1h bootstrap knob not another night dummy. KEEP if 1h composite beats "
        "-22.167. This single change starts from the current champion on the frozen 2014 "
        "test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. January RH>=70 Iws<2 RMSE may move from 42.65 toward "
        "24.0 to 38.0 versus persist-1 22.94. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen 2014 timestamps."
    ),
])
