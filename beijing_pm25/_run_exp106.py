"""Exp106 — CatBoost Plain add pm25_delta6 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add pm25_delta6 on Exp97 (CatBoost cycle 32/50)",
    "--add-feature", "pm25_delta6",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire recomputes January "
        "weekday persist>=150 by 6-hour episode trend and Thursday, not last fire's "
        "aggregate persist blob. New: January weekday persist>=150 with delta6>20 "
        "(still building over 6h) n=92 holds 10.1 percent of SSE, RMSE 61.11 versus "
        "persist-1 43.87, over-cleans pred_d -17.76 versus need -1.91. Falling 6h "
        "(delta6<-20) n=30 beats persist (45.87 versus 54.46). January Thursday "
        "persist>=150 n=47 is 6.8 percent SSE, RMSE 70.42 versus persist 50.96, "
        "pred_d -27.05 versus need -4.17. January weekday persist>=150 hours 18-21 "
        "n=26 need +26.38 pred_d +1.34. early_stopping=50 was inert. Patience and "
        "leaf floor stay closed."
    ),
    "--citations",
    (
        "Huang, Ru-Jin; Zhang, Yanlin; Bozzetti, Carlo; Ho, Kin-Fai; Cao, Jun-Ji; "
        "Han, Yongming; Daellenbach, Kaspar R.; Slowik, Jay G.; Platt, Stephen M.; "
        "Canonaco, Francesco; Zotter, Peter; Wolf, Robert; Pieber, Simone M.; Bruns, "
        "Emily A.; Crippa, Monica; Ciarelli, Giancarlo; Piazzalunga, Andrea; "
        "Schwikowski, Margit; Abbaszade, Guelcin; Schnelle-Kreis, Juergen; Zimmermann, "
        "Ralf; An, Zhisheng; Szidat, Soenke; Baltensperger, Urs; El Haddad, Imad and "
        "Prevot, Andre S. H. 2014 Nature 'High secondary aerosol contribution to "
        "particulate pollution during haze events in China' — secondary aerosol is "
        "30-77 percent of PM2.5 during Chinese haze, so a developing multi-hour "
        "episode keeps producing mass rather than mean-reverting in one hour. "
        "Relevance: Exp97 over-cleans January weekday persist>=150 hours whose "
        "6-hour trend is still building (delta6>20 RMSE 61.11 versus persist-1 43.87), "
        "and pm25_delta6 is one change from Exp97, not another patience knob after "
        "early_stopping=50 was inert."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pm25_delta6, defined as pm25_lag1 minus "
        "pm25_lag7, to the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, "
        "l2_leaf_reg 3, rh_magnus plus dewp_delta plus is_heating plus 24 lags) will "
        "cut 2013 val RMSE because the mechanism is an explicit 6-hour "
        "building-versus-falling episode state so January weekday persist>=150 hours "
        "that are still accumulating are not mean-reverted toward a collapse. Per "
        "Huang et al. 2014 secondary production during developing haze events keeps "
        "PM from dropping in one hour. Because early_stopping_rounds=50 was inert, "
        "this is the unused 6-hour trend feature not another patience knob. KEEP if "
        "1h composite beats -22.167. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. January weekday persist>=150 with delta6>20 "
        "RMSE may move from 61.11 toward 44.0 to 56.0 versus persist-1 43.87. A val "
        "RMSE above 22.25 is a miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
