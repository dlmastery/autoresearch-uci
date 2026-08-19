"""Exp109 — CatBoost Plain add evening_peak on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add evening_peak on Exp97 (CatBoost cycle 35/50)",
    "--add-feature", "evening_peak",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp108 is_severe DISCARD val "
        "22.313 test 20.899: 2014-01-16 93.08 to 100.50 worse, January weekday "
        "persist>=300 80.36 to 84.72 worse. New: the leftover with the opposite sign is "
        "January weekday persist 18-21 n=26 RMSE 58.70 versus persist-1 44.95, need "
        "+26.38 pred_d +1.34 under-predicts the evening rise. January weekday evening "
        "n=88 RMSE 43.89 versus persist 39.95, need +15.22 pred_d +3.59. Thursday persist "
        "18-21 actually beats persist (25.42 versus 29.52) so this is not the Jan-16 "
        "overnight bomb. Hour 20 year-round need +7.65 pred_d +4.96. is_severe stays closed."
    ),
    "--citations",
    (
        "Lelieveld, Jos; Evans, John S.; Fnais, Mohammed; Giannadaki, Despina and "
        "Pozzer, Andrea 2015 Nature 'The contribution of outdoor air pollution sources "
        "to premature mortality on a global scale' — urban PM2.5 is dominated by traffic "
        "and residential energy, so the evening commute is a 1h increment on top of an "
        "already-dirty hour rather than a collapse. Relevance: Exp97 under-predicts "
        "January weekday persist 18-21 (need +26.38 versus pred_d +1.34) and year-round "
        "hour 20 (need +7.65 versus pred_d +4.96) on the frozen 2014 nowcast, and "
        "evening_peak is one change from Exp97, not another lag1 threshold after "
        "is_severe missed 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding evening_peak, a binary equal to 1 when hour is 18 "
        "through 21, to the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, "
        "l2_leaf_reg 3, rh_magnus plus dewp_delta plus is_heating plus 24 lags) will "
        "cut 2013 val RMSE because the mechanism is an explicit rush-hour split so "
        "January weekday persist 18-21 hours are allowed to rise rather than stay near "
        "lag1. Per Lelieveld et al. 2015 that is traffic on top of an already-dirty "
        "hour. Because is_severe just failed, this is the unused evening-commute flag "
        "not another mega-haze threshold. KEEP if 1h composite beats -22.167. This "
        "single change starts from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. January weekday persist 18-21 RMSE may move "
        "from 58.70 toward 45.0 to 55.0 versus persist-1 44.95. A val RMSE above 22.25 "
        "is a miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
