"""Exp113 — CatBoost Plain add pm25_roll3mean on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add pm25_roll3mean on Exp97 (CatBoost cycle 39/50)",
    "--add-feature", "pm25_roll3mean",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire removes the two "
        "January bombs from the month blob, not last fire's SE-onset slice. New: January "
        "excluding 2014-01-16 hours 0-8 and 2014-01-31 hour 1 (n=679) BEATS persist, "
        "RMSE 29.19 versus 30.83, skill +5.3 percent. The 10 bomb hours are 7.5 percent "
        "SSE, RMSE 160.58 versus persist 114.72. After the +332 spike, hour 2 chases "
        "lag1=469 to pred 499 versus actual 344 (persist error 125, model 155). "
        "Post-onset January n=18 RMSE 89.11 versus persist 59.80. se_iws left 01-31 h1 "
        "inert. SE-Iws products, weather increments, lag1 flags stay closed."
    ),
    "--citations",
    (
        "Makridakis, Spyros; Spiliotis, Evangelos and Assimakopoulos, Vassilios 2018 "
        "arXiv 'The M4 Competition: Results, findings, conclusion and way forward' "
        "(arXiv:1810.11517) — simple smoothing of the recent window remains competitive "
        "on noisy series, so a 3-hour mean of PM lags is a more robust persist state "
        "than the last hour after a spike. Relevance: Exp97 chases 2014-01-31 hour 2 "
        "(pred 499 versus actual 344, lag1 469) after the +332 bomb, January excluding "
        "those 10 hours already beats persist (29.19 versus 30.83), and pm25_roll3mean "
        "is one change from Exp97, not another SE-Iws product after se_iws missed val."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pm25_roll3mean, the mean of pm25_lag1 through "
        "pm25_lag3, to the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, "
        "l2_leaf_reg 3, rh_magnus plus dewp_delta plus is_heating plus 24 lags) will "
        "cut 2013 val RMSE because the mechanism is a 3-hour robust persist so post-spike "
        "hours are not chased toward the last outlier. Per Makridakis et al. 2018 that "
        "is simple smoothing on a noisy series. Because se_iws just failed, this is the "
        "unused persist-smoothing feature not another SE product. KEEP if 1h composite "
        "beats -22.167. This single change starts from the current champion on the "
        "frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. 2014-01-31 hour 2 abs error may move from 155 "
        "toward 80 to 140 versus persist 125. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen 2014 timestamps."
    ),
])
