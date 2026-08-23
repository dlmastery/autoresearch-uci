"""Exp203 — FT-Transformer Pre-LN ff_factor=4 on Exp192 champion (FT cycle 29/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "ff_factor=4",
    "--description", "FT-Transformer Pre-LN ff_factor=4 on Exp192 recipe (FT cycle 29/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, collinear drops, patience, batch 16, and "
        "lr both sides closed. New: heating cv persist>=80 n=390 RMSE 31.15 versus persist "
        "30.14 (11.38 percent of SSE; need +3.68 pred_d +0.31) so winter calm-variable "
        "dirty hours capture only 8 percent of the rise and lose to persist, and Exp167 "
        "was 28.28 with pred_d +1.81. Unused change is ff_factor=4, not another lr."
    ),
    "--citations",
    (
        "Vaswani, Ashish; Shazeer, Noam; Parmar, Niki; Uszkoreit, Jakob; Jones, Llion; "
        "Gomez, Aidan N.; Kaiser, Lukasz and Polosukhin, Illia 2017 NeurIPS 'Attention "
        "Is All You Need' (arXiv:1706.03762) — the position-wise FFN uses inner width "
        "4d so each token mixes nonlinearly after attention, unlike this backbone's 2d "
        "default. Relevance: Exp192 dim_feedforward is 128; heating cv persist>=80 "
        "under-rises pred_d +0.31 versus need +3.68 at 31.15 versus persist 30.14 "
        "(Exp167 28.28); unused ff_factor=4 is one paper FFN widen, not another lr."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting ff_factor=4 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws) will cut 2013 val RMSE because the mechanism is a 4d position-wise FFN "
        "so cv x persist tokens mix enough for winter calm-variable hours to rise "
        "(need +3.68, Exp192 pred_d +0.31, RMSE 31.15 versus persist 30.14, Exp167 28.28). "
        "Per Vaswani et al. 2017 that is the paper FFN width. Because lr 5e-5 DISCARD, "
        "this is unused architecture not another lr. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if a 4d FFN lifts heating cv persist>=80 pred_d from +0.31 toward need "
        "+3.68. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
