"""Exp124 — CatBoost Plain add cv_inv on Exp97 1h champion (CatBoost 50/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add cv_inv on Exp97 (CatBoost cycle 50/50)",
    "--add-feature", "cv_inv",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire does not retry "
        "dow_sin (Exp123 val 22.360). New: cv persist>=150 n=505 is 12.4 percent of 2014 "
        "SSE, RMSE 28.95 versus persist 27.68, need +1.28 pred_d -0.01. 2013 val cv-dirty "
        "persist RMSE is 37.95 versus 2014 27.68, and 2013 cv-dirty need is -0.09 versus "
        "2014 +1.28. Mean inversion on that slice is 6.36. Keep dow. Add cv times "
        "inversion, not cyclic weekday or wind times Iws."
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
        "events in China' — stagnant moist residual layers trap winter PM2.5 when winds "
        "are calm. Relevance: Exp123 cyclic weekday missed val, but 2013 cv-dirty persist "
        "RMSE is 37.95 versus 2014 27.68 with need -0.09 versus +1.28, so cv_inv is one "
        "unused calm times inversion product from Exp97 after vent_index (Iws times inv) "
        "and se_iws failed."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding cv_inv = cbwd_cv times inversion_spread to the Exp97 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus "
        "dewp_delta plus is_heating plus 24 lags plus dow plus is_weekend) will cut 2013 "
        "val RMSE because the mechanism is scaling calm hours by TEMP-DEWP so 2013 "
        "cv-dirty need of -0.09 is not copied onto 2014's +1.28 rise. Per Huang et al. "
        "2014 that is stagnant residual-layer trapping. Because dow_sin just failed, this "
        "is unused calm-inversion product not another weekday encoding. KEEP if 1h "
        "composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if 2013 calm-haze hardness was a tax. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen timestamps."
    ),
])
