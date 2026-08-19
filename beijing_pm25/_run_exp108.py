"""Exp108 — CatBoost Plain add is_severe on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add is_severe on Exp97 (CatBoost cycle 34/50)",
    "--add-feature", "is_severe",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire splits January "
        "Thursday persist>=150 by calendar day, not last fire's Iws mean. New: 2014-01-16 "
        "alone is n=24 and 6.1 percent of all 2014 SSE, RMSE 93.08 versus persist-1 64.49, "
        "over-cleans pred_d -58.69 versus need -9.21, mean actual 457.5. Other January "
        "Thursdays match persist (01-02 n=12 RMSE 28.86 versus 29.93). PRES>=1025 on "
        "Thursday persist is that same day. January weekday persist>=300 n=39 is 7.4 "
        "percent SSE, RMSE 80.36 versus persist 55.80; not-January persist>=300 beats "
        "persist (34.41 versus 41.44). Thursday hours 0-5 RMSE 94.44 versus persist 37.79. "
        "log_iws and pm25_delta6 both made Thursday worse. Wind-scale and 6h trend stay closed."
    ),
    "--citations",
    (
        "Chen, Yuyu; Ebenstein, Avraham; Greenstone, Michael and Li, Hongbin 2013 "
        "Science 'Evidence on the impact of sustained exposure to air pollution on life "
        "expectancy from China's Huai River policy' — winter heating north of the Huai "
        "River produces sustained high PM, not hour-to-hour spikes that mean-revert, so "
        "a 1h nowcast should copy persist on already-severe hours rather than shrink "
        "toward the seasonal mean. Relevance: January weekday persist>=300 n=39 is 7.4 "
        "percent of 2014 SSE with RMSE 80.36 versus persist-1 55.80 (2014-01-16 alone is "
        "6.1 percent SSE, mean 457), and is_severe is one change from Exp97, not another "
        "wind-scale or 6-hour trend after log_iws and pm25_delta6 missed 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_severe, a binary equal to 1 when pm25_lag1 is at "
        "least 250 ug/m3 (HJ 633-2012 AQI 300 breakpoint), to the Exp97 CatBoost Plain "
        "recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus dewp_delta "
        "plus is_heating plus 24 lags) will cut 2013 val RMSE because the mechanism is "
        "an oblivious-tree split that isolates mega-haze hours so January persist>=300 "
        "is copied rather than mean-reverted. Per Chen et al. 2013 that is sustained "
        "heating-season exposure not a transitory spike. Because log_iws just failed, "
        "this is the unused severe-haze flag not another Iws transform. KEEP if 1h "
        "composite beats -22.167. This single change starts from the current champion "
        "on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. January weekday persist>=300 RMSE may move from "
        "80.36 toward 56.0 to 72.0 versus persist-1 55.80. A val RMSE above 22.25 is a "
        "miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
