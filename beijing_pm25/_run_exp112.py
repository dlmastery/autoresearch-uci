"""Exp112 — CatBoost Plain add se_iws on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add se_iws on Exp97 (CatBoost cycle 38/50)",
    "--add-feature", "se_iws",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire splits January onset "
        "by date and wind, not last fire's Jan16 overnight blob. New: 2014-01-31 hour 1 "
        "alone is 3.5 percent of all 2014 SSE, need +332 pred_d -16.14, SE wind, Iws 41.58. "
        "January onset SE n=10 is 6.9 percent SSE, RMSE 154.00 versus persist 149.49. "
        "corr(se*Iws, need | January onset)=0.56. January onset not-SE n=8 RMSE 120.01 "
        "versus persist 94.28. se_start hours actually beat persist. temp_delta left hour "
        "20 inert. Weather increments, lag1 flags, evening bins stay closed."
    ),
    "--citations",
    (
        "Ma, Zongwei; Hu, Xuefei; Sayer, Andrew M.; Levy, Robert; Zhang, Qiang; Xue, "
        "Yonggue; Tong, Shilu; Bi, Jun; Huang, Lei and Liu, Yang 2016 Science Advances "
        "'Satellite-Based Spatiotemporal Trends in PM2.5 Concentrations: China, "
        "2004-2013' — a persistent south-to-north PM2.5 gradient means a strong "
        "southerly wind can advect a polluted North China Plain air mass into Beijing "
        "in one hour, a jump local lag1 has not seen. Relevance: January onset SE hours "
        "hold 6.9 percent of 2014 SSE with RMSE 154 versus persist-1 149, the 2014-01-31 "
        "01:00 bomb is SE at Iws 41.58 with need +332, and se_iws is one change from "
        "Exp97, not another TEMP increment after temp_delta missed 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding se_iws, defined as cbwd_SE times Iws, to the Exp97 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus "
        "plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE because "
        "the mechanism is an explicit southerly transport flux so January onset hours "
        "with Iws above 10 are allowed a large positive increment instead of copying "
        "lag1. Per Ma et al. 2016 that is the south-to-north PM2.5 corridor. Because "
        "temp_delta just failed, this is the unused SE-wind product not another weather "
        "increment. KEEP if 1h composite beats -22.167. This single change starts from "
        "the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. January onset RMSE may move from 139.91 toward "
        "110.0 to 132.0 versus persist-1 127.93. A val RMSE above 22.25 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
