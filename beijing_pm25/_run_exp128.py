"""Exp128 — MLP shrink hidden 256-128-64 to 128-64-32 on Exp127 recipe (MLP cycle 4/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0.0001",
    "--set", "hidden=[128,64,32]",
    "--description", "MLP hidden 128-64-32 on Exp127 recipe (MLP cycle 4/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp127 MLP val 22.528 test "
        "20.773. New: hour 21 persist>=150 n=65 RMSE 58.72 versus CatBoost 50.21 and "
        "persist 56.30 (need +1.72 pred_d +5.15, 256-wide net over-cleans dirty evenings). "
        "|need|>=80 n=82 is 46.5 percent of Exp127 SSE versus 41.3 percent of Exp97, "
        "RMSE 139.40 versus CatBoost 131.19, pred_d -16.53 versus CatBoost -27.85. April "
        "29.24 nearly persist 29.32 versus CatBoost 27.06. Typical |need|<=10 already 7.03 "
        "versus CatBoost 8.35. Shrink unused width, do not retry dropout or wd."
    ),
    "--citations",
    (
        "Nakkiran, Preetum; Kaplun, Gal; Bansal, Yamini; Yang, Tristan; Barak, Boaz "
        "and Sutskever, Ilya 2020 ICLR 'Deep Double Descent: Where Bigger Models and "
        "More Data Hurt' (arXiv:1912.02292) — test error can rise again once a network "
        "crosses the interpolation threshold, so a wider MLP can generalize worse than "
        "a narrower one on the same data. Relevance: Exp127 keeps a 256-128-64 trunk "
        "(about 52000 weights on 43 features and 21725 train hours) and hour-21 "
        "persist>=150 plus |need|>=80 still lose to CatBoost, so shrinking hidden to "
        "128-64-32 is one unused capacity cut on the Exp127 recipe, not another dropout "
        "or weight-decay retry."
    ),
    "--hypothesis",
    (
        "We hypothesize that shrinking hidden from 256-128-64 to 128-64-32 on the "
        "Exp127 MLP recipe (dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, Smooth-L1, "
        "Exp97 features) will cut 2013 val RMSE because the mechanism is fewer "
        "first-layer units so 2010-12 year-specific evening and extreme-delta "
        "interactions cannot occupy unused capacity that then miss 2013 hour-21 "
        "persist>=150 and April-like hardness. Per Nakkiran et al. 2020 that is the "
        "interpolation side of double descent. Because dropout 0.3 and wd=1e-4 already "
        "probed regularizers, this is unused width not another dropout. KEEP if 1h "
        "composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.3 to 22.8 versus Exp97 20.735 and Exp127 20.773, val "
        "21.85 to 23.30, and composite -23.30 to -21.85. Val may move from 22.528 toward "
        "22.00 to 22.40 if unused width was a 2013 tax. A val RMSE above 22.90 is a miss. "
        "Ranges are ug/m3 on the frozen timestamps."
    ),
])
