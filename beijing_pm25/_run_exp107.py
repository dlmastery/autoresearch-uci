"""Exp107 — CatBoost Plain add log_iws on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add log_iws on Exp97 (CatBoost cycle 33/50)",
    "--add-feature", "log_iws",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp106 pm25_delta6 DISCARD "
        "val 22.345 test 20.671: January weekday persist>=150 only 56.12 to 55.27, "
        "building delta6>20 61.11 to 60.16, Thursday persist 70.42 to 72.21 worse. New: "
        "January Thursday persist>=150 n=47 is 6.8 percent SSE, RMSE 70.42 versus "
        "persist-1 50.96, mean Iws 4.13 versus 10.14 on other January weekday persist "
        "hours, mean actual 343.8. Calm-wind Thursday haze is the leftover, not 6-hour "
        "trend. Friday persist 59.01 to 48.77 under Exp106 but val still lost. Episode "
        "trend stays closed after one miss; patience stays closed."
    ),
    "--citations",
    (
        "Cai, Wenju; Li, Ke; Liao, Hong; Wang, Hejuan and Wu, Lixin 2017 Nature Climate "
        "Change 'Weather conditions conducive to Beijing severe haze more frequent under "
        "climate change' — Beijing severe haze requires weakened surface winds and a "
        "stagnant boundary layer, so high persist under calm Iws does not collapse in "
        "one hour the way ventilated hours do. Relevance: January Thursday persist>=150 "
        "hours have mean Iws 4.13 versus 10.14 on other January weekday persist hours "
        "and RMSE 70.42 versus persist-1 50.96 on the frozen 2014 nowcast, and log_iws "
        "is one change from Exp97, not another 6-hour trend after pm25_delta6 missed "
        "2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding log_iws, defined as log1p of Iws, to the Exp97 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus "
        "plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE because "
        "the mechanism is stretching the calm 0-5 m/s tail that depth-6 oblivious "
        "splits on raw Iws skip, so Thursday January persist>=150 hours are not treated "
        "as ventilated collapse cases. Per Cai et al. 2017 severe Beijing haze is a "
        "weak-wind regime. Because pm25_delta6 just failed 2013 val, this is the unused "
        "wind-scale feature not another episode-trend. KEEP if 1h composite beats "
        "-22.167. This single change starts from the current champion on the frozen "
        "2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. January Thursday persist>=150 RMSE may move "
        "from 70.42 toward 51.0 to 64.0 versus persist-1 50.96. A val RMSE above 22.25 "
        "is a miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
