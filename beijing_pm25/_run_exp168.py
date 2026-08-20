"""Exp168 — MLP huber_beta=20 on Exp167 residual recipe (MLP cycle 44/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "huber_beta=20",
    "--description", "MLP huber_beta=20 on Exp167 residual recipe (MLP cycle 44/50)",
    "--diagnosis",
    (
        "1h champion is now Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck, January 31.22 versus persist-1 33.58 and JJA 13.87, hour 20 32.68 "
        "versus persist 33.24, onset n=83 RMSE 110.28 losing to persist-1 107.80. Residual "
        "skips cut dirty-stable 13.13 to 11.99. New: onset hours need +87.40 but pred_d "
        "-0.60 (31.51 percent of SSE); 84 percent of onsets have pred_d under 10 and 40 "
        "percent predict below lag-1. Smooth-L1 beta=1 is MAE at this scale (test MAE "
        "11.06) so 5117 typical hours drown 83 onsets with equal unit gradients. Raise "
        "unused huber_beta, not skip-to-head."
    ),
    "--citations",
    (
        "Gneiting, Tilmann 2011 Journal of the American Statistical Association 'Making "
        "and Evaluating Point Forecasts' (arXiv:0912.0902) — absolute error is consistent "
        "for the conditional median while squared error is consistent for the mean, so an "
        "MAE-like loss reports persist on a right-skewed jump mixture. Relevance: Exp167 "
        "Smooth-L1 beta=1 is MAE at MAE 11.06, and onset n=83 still posts pred_d -0.60 "
        "versus need +87.40 at 110.28 versus persist 107.80, so raising unused huber_beta "
        "to 20 on the Exp167 residual recipe is one scoring-rule shift toward the mean, "
        "not another skip-to-head."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting huber_beta from 1.0 to 20 on the Exp167 residual MLP "
        "recipe (hidden 512-256-128, batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay "
        "1e-4, residual true, log_iws, month_sin, pm25_accel, vent_index, layer_norm off, "
        "clip=1.0) will cut 2013 val RMSE because the mechanism is a Smooth-L1 kink above "
        "typical MAE so onset residuals of 110 keep unit gradients while typical errors of "
        "7 get 7/20, lifting pred_d off -0.60. Per Gneiting 2011 that is mean-versus-median "
        "scoring. Because residual identity just locked persist on jumps, this is unused "
        "huber_beta not another skip. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 19.6 to 22.4 versus Exp167 20.072, val 21.40 to 23.00, and "
        "composite -23.00 to -21.40. Val may move from 21.972 toward 21.50 to 21.90 if "
        "MAE-median persist-lock on 2013 onsets was a val tax. A val RMSE above 22.80 is a "
        "miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
