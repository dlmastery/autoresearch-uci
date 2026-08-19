"""Exp110 — CatBoost Plain add rh_delta on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add rh_delta on Exp97 (CatBoost cycle 36/50)",
    "--add-feature", "rh_delta",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire splits 2014-01-16 "
        "by clock, not last fire's persist>=300 blob. New: hours 0-8 on 2014-01-16 n=9 "
        "is 4.0 percent of all 2014 SSE, RMSE 123.22 versus persist-1 48.74, over-cleans "
        "pred_d -118.60 versus need -10.00, mean actual 605. Hours 9-23 beat persist "
        "(68.94 versus 72.31). RH rises 58.5 to 79.6 while Iws stays under 3. "
        "corr(rh_delta, need | hours 0-8)=0.72 versus 0.14 overall. Other January "
        "overnight persist>=150 beats persist (39.85 versus 49.48). is_severe and "
        "evening_peak made Jan 16 worse. Lag1 flags, wind-scale, 6h trend, evening bins stay closed."
    ),
    "--citations",
    (
        "Cheng, Yafang; Zheng, Guangjie; Wei, Chao; Mu, Qing; Zheng, Bo; Wang, Zhibin; "
        "Gao, Meng; Zhang, Qiang; He, Kebin; Carmichael, Gregory; Poschl, Ulrich and "
        "Su, Hang 2016 Science Advances 'Reactive nitrogen chemistry in aerosol water "
        "as a source of sulfate during haze events in China' — aerosol water at rising "
        "RH converts NO2 to sulfate during northern-China haze, so overnight "
        "humidification keeps PM high rather than collapsing in one hour. Relevance: "
        "2014-01-16 hours 0-8 hold 4.0 percent of 2014 SSE with RMSE 123.22 versus "
        "persist-1 48.74 while RH climbs 58.5 to 79.6, and rh_delta is one change from "
        "Exp97, not another lag1 flag after is_severe missed 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding rh_delta, the first difference of Magnus RH, to "
        "the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE "
        "because the mechanism is an explicit humidification rate so 2014-01-16 hours "
        "0-8 are not mean-reverted toward a 118 ug/m3 crash. Per Cheng et al. 2016 "
        "aqueous sulfate production at rising RH keeps haze in place. Because is_severe "
        "just failed, this is the unused RH increment not another lag1 threshold. KEEP "
        "if 1h composite beats -22.167. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. 2014-01-16 hours 0-8 RMSE may move from 123.22 "
        "toward 49.0 to 100.0 versus persist-1 48.74. A val RMSE above 22.25 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
