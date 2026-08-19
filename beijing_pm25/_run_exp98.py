"""Exp98 — CatBoost Plain add heating_night on Exp97 is_heating 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add heating_night on Exp97 is_heating (CatBoost cycle 24/50)",
    "--add-feature", "heating_night",
    "--diagnosis",
    (
        "1h champion is Exp97 CatBoost: test 20.735, val 22.167 so val is the bottleneck, "
        "January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, onset n=83 "
        "RMSE 110.06 losing to persist-1 107.80. This fire recomputes Exp97 January moist "
        "hours by rain, wind, and clock, not last fire's aggregate RH>=70 blob. New: every "
        "January RH>=70 hour has Ir=0. January RH>=70 Iws<2 n=45 RMSE 42.65 versus Exp30 "
        "32.69 and persist-1 22.94 (skill -85.9 percent). January RH>=70 hours 0-5 n=37 "
        "RMSE 38.33 versus persist 18.85 (skill -103.4 percent), over-cleans pred_d -8.38 "
        "versus need -4.08. JJA RH>=70 Ir=0 is fine (14.93 versus persist 15.75). "
        "is_heating is already in; the unused cut is heating times night. month_sin stays "
        "closed."
    ),
    "--citations",
    (
        "Tie, Xuexi; Huang, Ru-Jin; Cao, Junji; Zhang, Qiang; Cheng, Yafang; Su, Hang; "
        "Chang, Di; Poeschl, Ulrich; Hoffmann, Thorsten; Dusek, Ulrike; Li, Guohui; "
        "Worsnop, Douglas R. and O'Dowd, Colin D. 2017 Nature Scientific Reports "
        "'Severe Pollution in China Amplified by Atmospheric Moisture' "
        "(doi:10.1038/s41598-017-11457-w) — nocturnal winter moisture collapses the "
        "mixing layer and amplifies haze, which is the opposite of summer wet removal, "
        "so a heating-night flag keeps 0-5 January RH from sharing the JJA moist cut. "
        "Relevance: Exp97 still RMSE 38.33 versus persist-1 18.85 on January RH>=70 "
        "hours 0-5 on the frozen 2014 nowcast, and adding heating_night is one change "
        "from Exp97, not another calendar sinusoid."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding heating_night, is_heating times the 18-06 clock, to "
        "the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE "
        "because the mechanism is one oblivious split on winter night so January RH>=70 "
        "hours 0-5 are not scored like JJA moist nights. Per Tie et al. 2017 that "
        "nocturnal moisture amplifies haze. Because is_heating just KEEPed and month_sin "
        "already failed, this is the unused night intersection not another season flag. "
        "KEEP if 1h composite beats -22.167. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. January RH>=70 hours 0-5 RMSE may move from 38.33 "
        "toward 20.0 to 32.0 versus persist-1 18.85. A val RMSE above 22.25 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
