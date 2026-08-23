"""Exp204 — FT-Transformer Pre-LN weight_decay=1e-6 on Exp192 champion (FT cycle 30/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "weight_decay=1e-6",
    "--description", "FT-Transformer Pre-LN weight_decay=1e-6 on Exp192 recipe (FT cycle 30/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, collinear drops, patience, batch, lr both "
        "sides, and ff_factor=4 closed. New: PRES>=1025 persist>=150 n=413 RMSE 41.99 versus "
        "persist 40.56 (21.90 percent of SSE; need -3.20 pred_d -10.12) so high-pressure "
        "dirty hours over-clean 3x the increment and lose to persist, and Exp167 was 38.29 "
        "with pred_d -8.97. Unused change is weight_decay=1e-6, not another FFN widen."
    ),
    "--citations",
    (
        "Loshchilov, Ilya and Hutter, Frank 2019 ICLR 'Decoupled Weight Decay "
        "Regularization' (arXiv:1711.05101) — AdamW applies L2 to weights separately from "
        "the adaptive step, so too-large decay shrinks rare-regime tokens and underfits "
        "anticyclone hours. Relevance: Exp192 wd 1e-5 still over-cleans PRES>=1025 "
        "persist>=150 pred_d -10.12 versus need -3.20 at 41.99 versus persist 40.56 "
        "(Exp167 38.29); unused weight_decay=1e-6 is one weaker decay, not another FFN."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting weight_decay=1e-6 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, epochs 100, patience 15, warmup 10, cbwd_prev_NW, rh_iws, 2d FFN) will "
        "cut 2013 val RMSE because the mechanism is weaker decoupled L2 so PRES x persist "
        "tokens are not shrunk toward always-drop on anticyclone hours (need -3.20, Exp192 "
        "pred_d -10.12, RMSE 41.99 versus persist 40.56, Exp167 38.29). Per Loshchilov and "
        "Hutter 2019 that is AdamW decay. Because ff_factor=4 DISCARD and wd 1e-4 already "
        "closed, this is unused weaker decay not another FFN. KEEP if 1h composite beats "
        "-21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if weaker decay lifts PRES>=1025 persist>=150 pred_d from -10.12 toward "
        "need -3.20. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
