"""Exp118 — CatBoost Plain model_size_reg=1.0 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain model_size_reg=1.0 on Exp97 (CatBoost cycle 44/50)",
    "--set", "model_size_reg=1.0",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire does not drop dow "
        "(Exp117 near-miss val 22.212, Thursday 20.85 to 21.82). New: hour-20 Wednesday "
        "n=49 RMSE 73.90 versus persist 74.10 (need +15.43 pred_d +3.18), and hour-20 "
        "Wednesday mean PM is train 107.6 versus 2013 val 84.6 versus 2014 114.0. Friday "
        "18-21 n=189 RMSE 26.96 versus persist 24.54 with corr(pred_d, need) -0.144. 2013 "
        "Friday persist 27.5 is the hardest val weekday. Keep dow and is_weekend; "
        "regularize leaf size."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna "
        "Veronika and Gulin, Andrey 2018 NeurIPS 'CatBoost: unbiased boosting with "
        "categorical features' (arXiv:1706.09516) — oblivious trees share splits across "
        "a level so a weekday-hour cut is reused, and model_size_reg penalizes large "
        "combinations so those shared leaves shrink. Relevance: Exp117 showed dropping "
        "dow hurts 2014 Thursday, but hour-20 Wednesday train 107.6 reverses to 2013 "
        "84.6 and Friday evening increment corr is -0.144, so raising model_size_reg "
        "from 0.5 to 1.0 keeps weekday features while shrinking 2010-12 weekday-hour "
        "leaves, not another drop-dow or Iws clip."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting model_size_reg from the CatBoost default 0.5 to 1.0 "
        "on the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags plus dow plus is_weekend) "
        "will cut 2013 val RMSE because the mechanism is shrinking large weekday-hour "
        "oblivious leaves whose hour-20 Wednesday mean reverses from train 107.6 to 2013 "
        "84.6 so val is not pulled toward 2010-12 evening-haze calendars. Per "
        "Prokhorenkova et al. 2018 that is model-size regularization. Because Exp117 "
        "drop dow near-missed val and hurt Thursday, this is unused leaf-size "
        "regularizer not another weekday drop. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if weekday-hour leaf size was a 2013 tax. A val RMSE above 22.25 is a miss. "
        "Ranges are ug/m3 on the frozen timestamps."
    ),
])
