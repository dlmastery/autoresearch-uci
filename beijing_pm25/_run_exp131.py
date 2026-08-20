"""Exp131 — MLP epochs 50 to 80 on Exp130 recipe (MLP cycle 7/50)."""
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
    "--set", "epochs=80",
    "--description", "MLP epochs=80 on Exp130 recipe (MLP cycle 7/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp130 MLP val 22.527 test "
        "20.457 (best 2014) but val-test gap 2.07 versus CatBoost 1.432. New: hour 18 "
        "persist>=100 n=103 RMSE 32.58 versus CatBoost 27.03 and persist 36.50, need "
        "-1.04 pred_d +1.82. Hour 18 overall 26.99 versus CatBoost 24.68 is 7.27 percent "
        "of Exp130 SSE versus 5.91 percent of Exp97. February hour 18 50.6 versus "
        "CatBoost 37.5. Smooth-L1 early-stop under-weights those tails. Stretch unused "
        "cosine epochs, do not retry batch 8."
    ),
    "--citations",
    (
        "Loshchilov, Ilya and Hutter, Frank 2017 ICLR 'SGDR: Stochastic Gradient "
        "Descent with Warm Restarts' (arXiv:1608.03983) — cosine annealing sets the "
        "step-size path from T_max, so stretching the epoch budget from 50 to 80 slows "
        "the decay and leaves larger mid-training Adam steps for residuals that Huber "
        "loss saturates. Relevance: Exp130 early-stops on Smooth-L1 not RMSE, hour-18 "
        "persist>=100 still loses CatBoost 32.58 versus 27.03, and the val-test gap "
        "widened to 2.07, so raising epochs to 80 is one unused cosine-budget change "
        "on the Exp130 recipe, not another batch or dropout."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting epochs from 50 to 80 on the Exp130 MLP recipe "
        "(batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, "
        "Smooth-L1, Exp97 features) will cut 2013 val RMSE because the mechanism is a "
        "slower cosine T_max so hour-18 persist>=100 Huber-saturated residuals still "
        "move after Smooth-L1 has flattened. Per Loshchilov and Hutter 2017 that is "
        "cosine T_max. Because batch 16 just won 2014 test and missed the val gate, this "
        "is unused epochs not another batch. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.2 to 22.5 versus Exp97 20.735 and Exp130 20.457, val "
        "21.80 to 23.10, and composite -23.10 to -21.80. Val may move from 22.527 toward "
        "22.00 to 22.40 if a slower cosine fits 2013 evening tails. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
