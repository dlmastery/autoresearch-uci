"""Exp123 — CatBoost Plain add dow_sin on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add dow_sin on Exp97 (CatBoost cycle 49/50)",
    "--add-feature", "dow_sin",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire does not retry "
        "is_morning (Exp122 val 22.346). New: corr(dow_sin, y) is -0.078 on 2013 val versus "
        "+0.051 on 2011 and -0.046 on 2012, a sign flip cyclic weekday does not share with "
        "numeric dow (val 0.065, train near 0). Test residual corr with dow_sin is -0.027. "
        "Thursday still loses persist 20.85 versus 20.75. Keep dow. Add sine, not an hour bin."
    ),
    "--citations",
    (
        "Petnehazi, Gabor 2019 arXiv 'A brief overview of encoding categorical features' "
        "(arXiv:1902.04932) — a sine of a periodic integer maps adjacent weekdays onto a "
        "smooth circle so trees need not isolate a single Thursday leaf. Relevance: Exp117 "
        "drop dow near-missed val and Exp122 morning bins missed, but 2013 corr(dow_sin, y) "
        "is -0.078 versus 2011 +0.051 so adding dow_sin while keeping numeric dow is one "
        "unused cyclic encoding from Exp97, not another hour dummy or wind product."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding dow_sin = sin(2 pi dow / 7) to the Exp97 CatBoost Plain "
        "recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus dewp_delta plus "
        "is_heating plus 24 lags plus dow plus is_weekend) will cut 2013 val RMSE because "
        "the mechanism is a smooth weekday circle so 2013's negative cyclic correlation is "
        "not forced through a numeric Thursday split fit on 2010-12 near-zero corr. Per "
        "Petnehazi 2019 that is cyclic encoding. Because is_morning just failed, this is "
        "unused weekday sine not another hour bin. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if numeric dow leaves were a 2013 tax. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen timestamps."
    ),
])
