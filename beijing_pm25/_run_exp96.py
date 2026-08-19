"""Exp96 — CatBoost Plain add dewp_delta on Exp91 rh_magnus 1h recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add dewp_delta on Exp91 rh_magnus (CatBoost cycle 22/50)",
    "--backbone", "catboost",
    "--add-feature", "rh_magnus",
    "--add-feature", "dewp_delta",
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
        "persist-1 107.80. This fire recomputes Exp91 residuals on Friday and dewpoint "
        "tendency, not last fire's high-PRES dirty blob. Exp91 val 22.449 is 0.052 from "
        "KEEP. New: Friday n=1119 RMSE 24.81 versus Exp30 23.59 and persist-1 24.13 "
        "(skill -2.8 percent). Hour-1 29.71 versus persist 28.19. NE persist>=150 weekday "
        "n=128 RMSE 41.91 versus Exp30 34.61. dewp-rise persist>=150 n=378 RMSE 36.61 "
        "versus persist 35.88, over-cleans pred_d -4.25 versus need +0.51. dewp_delta "
        "correlates 0.16 with the 1h increment; pres_delta was 0.00. Wind dummy and "
        "random_strength stay closed."
    ),
    "--citations",
    (
        "Tie, Xuexi; Huang, Ru-Jin; Cao, Junji; Zhang, Qiang; Cheng, Yafang; Su, Hang; "
        "Chang, Di; Poeschl, Ulrich; Hoffmann, Thorsten; Dusek, Ulrike; Li, Guohui; "
        "Worsnop, Douglas R. and O'Dowd, Colin D. 2017 Nature Scientific Reports "
        "'Severe Pollution in China Amplified by Atmospheric Moisture' "
        "(doi:10.1038/s41598-017-11457-w) — rising dewpoint is moist inflow that static "
        "Magnus RH already saturates, so the 1h tendency is the unused moisture clock. "
        "Relevance: Exp91 still RMSE 36.61 versus persist-1 35.88 on dewpoint-rise "
        "persist>=150 hours on the frozen 2014 nowcast (pred_d -4.25 versus need +0.51), "
        "and adding dewp_delta is one change from Exp91, not another wind dummy or "
        "split-score noise."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding dewp_delta, the 1h DEWP difference, to the Exp91 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus "
        "plus inversion_spread plus pm25_delta1 plus 24 lags) will cut 2013 val RMSE "
        "because the mechanism is one oblivious split on rising dewpoint so dirty hours "
        "with moist inflow are not treated as already-wet air about to clean out. Per "
        "Tie et al. 2017 that moisture tendency amplifies PM. Because cbwd_prev_NW and "
        "random_strength already failed, this is the unused 1h dewpoint clock not another "
        "HP. KEEP if 1h composite beats -22.397. This single change starts from the "
        "current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.6 to 21.8 versus Exp30 20.945, val 22.05 to 22.60, and "
        "composite -22.70 to -22.05. dewp-rise persist>=150 RMSE may move from 36.61 "
        "toward 33.5 to 36.0 versus persist-1 35.88. A val RMSE above 22.55 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
