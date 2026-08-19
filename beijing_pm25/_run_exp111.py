"""Exp111 — CatBoost Plain add temp_delta on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add temp_delta on Exp97 (CatBoost cycle 37/50)",
    "--add-feature", "temp_delta",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire splits 2014-01-16 "
        "hours 0-8 by wind, not last fire's RH-rise blob. New: hours 0-8 not-NW n=6 is "
        "3.3 percent of 2014 SSE, RMSE 137.65 versus persist 42.70, need +9.33 pred_d "
        "-120.74 wrong sign. cv subset n=3 RMSE 151.75 versus persist 52.38. Other "
        "January overnight persist>=150 beats persist (39.85 versus 49.48); cv "
        "persist>=300 hours 0-8 excluding Jan 16 matches persist (34.04 versus 34.75). "
        "January onset n=18 is 10.3 percent SSE, RMSE 139.91 versus persist 127.93. "
        "Hour 20 still need +7.65 pred_d +4.96 after evening_peak DISCARD. rh_delta left "
        "hours 0-8 inert. RH increments, lag1 flags, evening bins stay closed."
    ),
    "--citations",
    (
        "Petaja, Tuukka; Jarvi, Leena; Kerminen, Veli-Matti; Ding, Aijun; Sun, Jianing; "
        "Nie, Wei; Kujansuu, Joni; Virkkula, Aki; Yang, Xuguang; Fu, Congbin; "
        "Zilitinkevich, Sergej and Kulmala, Markku 2016 Science Advances 'Enhanced air "
        "pollution via aerosol-boundary layer feedback in China' — a temperature drop "
        "shallows the boundary layer so PM rises in the evening and stays trapped "
        "overnight rather than mixing out in one hour. Relevance: Exp97 under-predicts "
        "hour 20 (need +7.65 versus pred_d +4.96) after evening_peak missed val, and "
        "temp_delta is one change from Exp97, not another RH increment after rh_delta "
        "left 2014-01-16 hours 0-8 at RMSE 122.74 versus persist-1 48.74."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding temp_delta, the first difference of TEMP, to the "
        "Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE "
        "because the mechanism is an explicit cooling-driven boundary-layer increment "
        "so hour-20 and stagnant overnight hours are not treated as ventilated collapses. "
        "Per Petaja et al. 2016 that is aerosol-boundary-layer feedback. Because rh_delta "
        "just failed the leftover, this is the unused TEMP increment not another RH rate. "
        "KEEP if 1h composite beats -22.167. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Hour 20 RMSE may move from 32.48 toward 28.0 "
        "to 32.0 versus persist-1 33.24. A val RMSE above 22.25 is a miss. Ranges are "
        "ug/m3 on the frozen 2014 timestamps."
    ),
])
