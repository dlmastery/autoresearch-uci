"""Exp130 — MLP batch_size 32 to 16 on Exp127 recipe (MLP cycle 6/50)."""
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
    "--description", "MLP batch_size=16 on Exp127 recipe (MLP cycle 6/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp127 MLP val 22.528 test "
        "20.773. Exp129 lr=1e-4 underfit. New: SE wind n=2937 is 36.9 percent of hours "
        "but 43.6 percent of Exp127 SSE versus 41.1 percent of Exp97, RMSE 22.56 versus "
        "CatBoost 21.87 and persist 23.27, need +2.51 pred_d +0.77 (under-builds). SE "
        "persist>=150 n=562 RMSE 32.65 versus CatBoost 30.59. Rain Ir>0 n=260 24.89 versus "
        "CatBoost 21.51. Shrink unused batch, do not retry lr 1e-4 or width."
    ),
    "--citations",
    (
        "Keskar, Nitish Shirish; Mudigere, Dheevatsa; Nocedal, Jorge; Smelyanskiy, "
        "Mikhail and Tang, Ping Tak Peter 2017 ICLR 'On Large-Batch Training for Deep "
        "Learning: Generalization Gap and Sharp Minima' (arXiv:1609.04836) — small-batch "
        "SGD finds flatter minima that transfer, while larger batches converge to sharp "
        "basins that miss a shifted validation year. Relevance: Exp127 trains at batch "
        "32 with a 1.755 val-test gap versus CatBoost 1.432, SE wind owns 43.6 percent "
        "of MLP SSE, and lr=1e-4 just underfit, so cutting batch_size from 32 to 16 is "
        "one unused noise lever on the Exp127 recipe, not another learning-rate shrink."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting batch_size from 32 to 16 on the Exp127 MLP recipe "
        "(hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, Smooth-L1, "
        "Exp97 features) will cut 2013 val RMSE because the mechanism is noisier SGD "
        "so 2010-12 SE-wind year-specific basins cannot sharpen enough to miss 2013 "
        "southerly build hours. Per Keskar et al. 2017 that is the small-batch flat-minima "
        "gap. Because lr=1e-4 just underfit and width shrink failed, this is unused batch "
        "not another lr. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.3 to 22.6 versus Exp97 20.735 and Exp127 20.773, val "
        "21.85 to 23.20, and composite -23.20 to -21.85. Val may move from 22.528 toward "
        "22.00 to 22.40 if batch-32 sharp minima were a 2013 tax. A val RMSE above 22.90 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
