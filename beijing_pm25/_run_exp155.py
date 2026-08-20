"""Exp155 — MLP add heating_build on Exp136 recipe (MLP cycle 31/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0.0001",
    "--set", "batch_size=16",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--add-feature", "heating_build",
    "--description", "MLP add heating_build on Exp136 recipe (MLP cycle 31/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. HP opposites "
        "closed. New: heating need>20 n=261 RMSE 55.12 versus CatBoost 55.19 and persist "
        "54.39, need +43.56 pred_d +1.92 so winter builds stay persist-locked (23.7 percent "
        "of SSE). is_heating and delta1 are additive. Add unused heating_build, do not "
        "retry wd=0."
    ),
    "--citations",
    (
        "Huang, Ru-Jin; Zhang, Yanlin; Bozzetti, Carlo; Ho, Kin-Fai; Cao, Jun-Ji; Han, "
        "Yongming; Daellenbach, Kaspar R.; Slowik, Jay G.; Platt, Stephen M.; Canonaco, "
        "Francesco; Zotter, Peter; Wolf, Robert; Pieber, Simone M.; Bruns, Emily A.; "
        "Crippa, Monica; Ciarelli, Giancarlo; Piazzalunga, Andrea; Schwikowski, Margit; "
        "Abbaszade, Gulcin; Schnelle-Kreis, Jurgen; Zimmermann, Ralf; An, Zhisheng; "
        "Szidat, Sonke; Baltensperger, Urs; El Haddad, Imad and Prevot, Andre S. H. 2014 "
        "Nature 'High secondary aerosol contribution to particulate pollution during haze "
        "events in China' — winter haze is coal-heating plus secondary chemistry, so a "
        "rising hour in the heating season is a different regime than a summer rise. "
        "Relevance: Exp136 already has is_heating, pm25_delta1, and pm25_accel additively "
        "but heating need>20 still persist-locks pred_d +1.92 versus need +43.56, so adding "
        "unused heating times max(delta1,0) is one winter-momentum product on the Exp136 "
        "recipe, not another weight decay."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding heating_build on the Exp136 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus is_heating "
        "times max of pm25_delta1 and zero) will cut 2013 val RMSE because the mechanism "
        "is an explicit winter-rising product so heating need>20 hours are not treated "
        "as summer mean-reverting delta1. Per Huang et al. 2014 that is coal-heating haze. "
        "Because wd=0 just failed stuck hours, this is unused heating_build not another "
        "L2. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if additive heating plus delta1 was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
