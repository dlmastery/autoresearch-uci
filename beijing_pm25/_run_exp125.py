"""Exp125 — Isolate MLP default recipe on Exp97 1h features (MLP cycle 1/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--description", "MLP default 256-128-64 on Exp97 features (MLP cycle 1/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80 (29.4 percent of SSE). CatBoost "
        "50/50 is complete (Exp124 cv_inv DISCARD). New: typical hours with |need|<=10 "
        "n=5117 RMSE 8.35 versus persist 5.08 (trees over-adjust), while |need|>=30 n=689 "
        "beats persist 59.01 versus 67.57. persist>=q67 is 67.1 percent of SSE. corr of "
        "|need| with |err| is 0.866. Isolate MLP, do not mix CatBoost HPs."
    ),
    "--citations",
    (
        "Gu, Shihao; Kelly, Bryan and Xiu, Dacheng 2020 RFS 'Empirical Asset Pricing via "
        "Machine Learning' (arXiv:1802.09003) — a fixed-depth MLP with dropout is the "
        "neural tabular floor against trees on standardized features. Relevance: CatBoost "
        "50/50 is done and typical |need|<=10 hours lose to persist 8.35 versus 5.08 so "
        "oblivious leaves over-adjust small increments, and switching to the default "
        "256-128-64 dropout-0.2 AdamW recipe on Exp97 features is one backbone change, "
        "not another CatBoost product or regularizer."
    ),
    "--hypothesis",
    (
        "We hypothesize that replacing Exp97 CatBoost Plain with the default MLP "
        "(hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-5, Smooth-L1, "
        "50 epochs, patience 10) on the same Exp97 features will cut 2013 val RMSE "
        "because the mechanism is a continuous residual surface so typical |need|<=10 "
        "hours are not forced through piecewise-constant leaves that over-adjust versus "
        "persist 5.08. Per Gu et al. 2020 that is the MLP tabular floor. Because CatBoost "
        "50/50 just closed, this is unused backbone isolation not another tree feature. "
        "KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.8 to 28.0 versus Exp97 20.735, val 22.2 to 30.0, "
        "and composite -30.0 to -22.10. First MLP isolation may miss the CatBoost "
        "champion the way Exp20 LightGBM and Exp21 CatBoost first tries did. A val RMSE "
        "above 24.0 is a large miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
