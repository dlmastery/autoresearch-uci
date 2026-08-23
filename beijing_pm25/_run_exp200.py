"""Exp200 — FT-Transformer Pre-LN patience=25 on Exp192 champion (FT cycle 26/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "patience=25",
    "--description", "FT-Transformer Pre-LN patience=25 on Exp192 recipe (FT cycle 26/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Patience=8 underfit. New: need 20-50 n=515 RMSE 29.68 "
        "versus persist 30.83 (13.64 percent of SSE; need +29.90 pred_d +2.42) so moderate "
        "jumps capture only 8 percent of the rise, Exp167 was 28.91 with pred_d +3.31, and "
        "patience=8 made it 31.51 with pred_d +0.95. Unused change is patience=25, not "
        "nearby 5/10."
    ),
    "--citations",
    (
        "Loshchilov, Ilya and Hutter, Frank 2017 ICLR 'SGDR: Stochastic Gradient Descent "
        "with Warm Restarts' (arXiv:1608.03983) — a cosine-annealed schedule can keep "
        "improving after a long plateau, so a longer early-stop window lets later cosine "
        "epochs finish. Relevance: Exp192 already uses cosine after warmup 10, moderate "
        "jumps still predict +2.42 versus need +29.90 at 29.68 versus persist 30.83, and "
        "patience=8 underfit them to pred_d +0.95; setting unused patience=25 on Exp192 is "
        "one longer cosine wait, not nearby 5/10."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting patience=25 on the Exp192 Pre-LN FT champion (d_model "
        "64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, warmup 10, cbwd_prev_NW, rh_iws) will cut 2013 val "
        "RMSE because the mechanism is waiting ten more cosine-anneal epochs so moderate "
        "jumps keep rising instead of stopping at a 15-epoch plateau (need +29.90, Exp192 "
        "pred_d +2.42, RMSE 29.68 versus persist 30.83). Per Loshchilov and Hutter 2017 that "
        "is a later cosine valley. Because patience=8 underfit those jumps, this is unused "
        "longer wait not nearby 5/10. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if later cosine epochs lift moderate-jump pred_d from +2.42. A val RMSE "
        "above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
