"""Exp201 — FT-Transformer Pre-LN batch_size=16 on Exp192 champion (FT cycle 27/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "batch_size=16",
    "--description", "FT-Transformer Pre-LN batch_size=16 on Exp192 recipe (FT cycle 27/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Patience both sides closed. New: hour20 persist>=80 "
        "n=141 RMSE 48.51 versus persist 49.10 (9.97 percent of SSE; need +10.87 pred_d "
        "+3.53) so evening dirty hours capture only 32 percent of the rise, and Exp167 "
        "batch-16 was pred_d +4.75. Unused change is batch_size=16, not another early-stop."
    ),
    "--citations",
    (
        "Keskar, Nitish Shirish; Mudigere, Dheevatsa; Nocedal, Jorge; Smelyanskiy, Mikhail "
        "and Tang, Ping Tak Peter 2017 ICLR 'On Large-Batch Training for Deep Neural "
        "Networks: Generalization Gap and Sharp Minima' (arXiv:1609.04836) — large-batch "
        "SGD converges to sharp minima that generalize worse, so halving batch size adds "
        "gradient noise that prefers flatter solutions. Relevance: Exp192 batch 32 still "
        "under-rises hour20 persist>=80 pred_d +3.53 versus need +10.87 at 48.51 versus "
        "persist 49.10, and val 21.948 is the bottleneck; unused batch_size=16 on Exp192 "
        "is one small-batch flatten, not another patience."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting batch_size=16 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, rh_iws) will "
        "cut 2013 val RMSE because the mechanism is noisier SGD so evening dirty hours rise "
        "more instead of sitting in a sharp under-rise (need +10.87, Exp192 pred_d +3.53, "
        "RMSE 48.51 versus persist 49.10). Per Keskar et al. 2017 that is a flatter minimum. "
        "Because patience 8 and 25 DISCARD, this is unused small-batch not another "
        "early-stop. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if noisier steps lift hour20 persist>=80 pred_d from +3.53. A val RMSE "
        "above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
