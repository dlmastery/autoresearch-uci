"""Exp127 — MLP weight_decay 1e-4 on Exp125 recipe (MLP cycle 3/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0.0001",
    "--description", "MLP weight_decay=1e-4 on Exp125 default recipe (MLP cycle 3/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp125 MLP val 22.623 test "
        "20.648. Exp126 dropout 0.3 inverted val. New: collapse n=162 RMSE 78.82 versus "
        "CatBoost 74.05 and persist 97.87, pred_d -22.24 versus CatBoost -24.95 versus "
        "need -86.31 (MLP under-cleans crashes). December 21.58 versus CatBoost 21.02. "
        "Hour 1 27.90 now beats persist 28.19. Do not retry dropout. Raise AdamW L2."
    ),
    "--citations",
    (
        "Loshchilov, Ilya and Hutter, Frank 2019 ICLR 'Decoupled Weight Decay "
        "Regularization' (arXiv:1711.05101) — AdamW applies weight decay outside the "
        "adaptive step so L2 actually shrinks hidden weights instead of being absorbed "
        "into Adam's second moment. Relevance: Exp126 dropout 0.3 helped 2014 test and "
        "taxed 2013 val, and MLP collapse pred_d is only -22.24 versus need -86.31, so "
        "raising weight_decay from 1e-5 to 1e-4 is one unused AdamW regularizer on the "
        "Exp125 recipe, not another dropout or CatBoost HP."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting weight_decay from 1e-5 to 1e-4 on the Exp125 MLP "
        "recipe (hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, Smooth-L1, Exp97 features) "
        "will cut 2013 val RMSE because the mechanism is decoupled L2 so 2010-12 "
        "year-specific hidden weights cannot grow large enough to miss 2013 crash and "
        "December hours. Per Loshchilov and Hutter 2019 that is AdamW weight decay. "
        "Because dropout 0.3 just failed val, this is unused L2 not another dropout. "
        "KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.3 to 22.5 versus Exp97 20.735 and Exp125 20.648, val "
        "21.90 to 23.20, and composite -23.20 to -21.90. Val may move from 22.623 toward "
        "22.00 to 22.40 if hidden-weight growth was a 2013 tax. A val RMSE above 22.80 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
