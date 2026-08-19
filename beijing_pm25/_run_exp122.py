"""Exp122 — CatBoost Plain add is_morning on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add is_morning on Exp97 (CatBoost cycle 48/50)",
    "--add-feature", "is_morning",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire does not retry "
        "nw_iws (Exp121 val 22.240). New: hour 8-9 n=663 RMSE 18.16 versus persist 18.26, "
        "need -0.20 pred_d -1.47 (over-clean). 2013 val hour 8-9 need is -2.37 versus 2014 "
        "-0.20 versus 2010 +0.05. January hour 8-9 need +0.26 pred_d -2.80. Keep dow and "
        "hour_sin. Add a morning 7-9 flag, not evening_peak or wind times Iws."
    ),
    "--citations",
    (
        "Huang, Ru-Jin; Zhang, Yanlin; Bozzetti, Carlo; Ho, Kin-Fai; Cao, Jun-Ji; Han, "
        "Yongming; Daellenbach, Kaspar R.; Slowik, Jay G.; Platt, Stephen M.; Canonaco, "
        "Francesco; Zotter, Peter; Wolf, Robert; Pieber, Simone M.; Bruns, Emily A.; "
        "Crippa, Monica; Ciarelli, Giancarlo; Piazzalunga, Andrea; Schwikowski, Margit; "
        "Abbaszade, Guelcin; Schnelle-Kreis, Juergen; Zimmermann, Ralf; An, Zhisheng; "
        "Szidat, Soenke; Baltensperger, Urs; El Haddad, Imad and Prevot, Andre S. H. 2014 "
        "Nature 'High secondary aerosol contribution to particulate pollution during haze "
        "events in China' — nocturnal chemistry and the morning residual-layer breakup "
        "set the 07-09 increment. Relevance: Exp121 nw_iws missed val, but 2013 morning "
        "need is -2.37 versus 2014 -0.20 so cyclic hour_sin is too smooth for that "
        "breakup, and is_morning is one unused 7-9 flag from Exp97 after evening_peak "
        "failed on 18-21."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_morning (hour 7 to 9) to the Exp97 CatBoost Plain "
        "recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus dewp_delta "
        "plus is_heating plus 24 lags plus dow plus is_weekend) will cut 2013 val RMSE "
        "because the mechanism is an explicit morning-breakup split so 2013 hour 8-9 "
        "need of -2.37 is not forced through hour_sin leaves fit on 2014-like near-zero "
        "mornings. Per Huang et al. 2014 that is residual-layer breakup. Because nw_iws "
        "just failed, this is unused morning-hour identity not another wind product. "
        "KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if 2013 morning fall was a tax. A val RMSE above 22.25 is a miss. Ranges are "
        "ug/m3 on the frozen timestamps."
    ),
])
