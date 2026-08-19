"""Exp116 — CatBoost Plain replace Iws with iws_clip100 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain replace Iws with iws_clip100 on Exp97 (CatBoost cycle 42/50)",
    "--add-feature", "iws_clip100",
    "--drop-feature", "Iws",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire compares Iws tails "
        "across splits, not last fire's lag24 corr. New: train Iws mean 26.82 with 7.2 "
        "percent of hours above 100 versus val 21.42 and 4.7 percent and test 19.44 and "
        "4.1 percent. Train Iws p99 is 273 versus val p90 only 51. Snow corr is 0.055 on "
        "2013 val versus 0.007 train so snow stays. Exp115 showed long lags help val. "
        "is_janfeb missed val. Lag-window cuts and calendar subsets stay closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna "
        "Veronika and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with "
        "Categorical Features' (arXiv:1706.09516) — oblivious trees share one split "
        "threshold on Iws across every leaf, so a 2010-12 storm tail (train p99 273) "
        "can warp all 2013 leaves where Iws is calmer (mean 21.42). Relevance: 2013 val "
        "persist is 24.50 versus 2014 test 22.32 and Exp97 skill is already +9.5 percent "
        "on val, and replacing Iws with min(Iws,100) is one change from Exp97, not "
        "another lag-window cut after drop lag13-24 slightly hurt 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that replacing Iws with iws_clip100, defined as min(Iws, 100), "
        "on the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE "
        "because the mechanism is blocking 2010-12 dust-storm tail splits that oblivious "
        "trees share globally so 2013's calmer wind climate is not scored as weak-wind "
        "haze. Per Prokhorenkova et al. 2018 that is shared Iws thresholds. Because drop "
        "lag13-24 just failed val, this is unused Iws winsorizing not another lag cut. "
        "KEEP if 1h composite beats -22.167. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if the train Iws tail was a 2013 tax. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen timestamps."
    ),
])
