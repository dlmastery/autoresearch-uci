"""Exp146 — MLP add dow_sin on Exp136 recipe (MLP cycle 22/50)."""
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
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--add-feature", "dow_sin",
    "--description", "MLP add dow_sin on Exp136 recipe (MLP cycle 22/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: Wednesday n=1149 RMSE "
        "25.99 versus CatBoost 25.07 and persist 27.60, need +1.25 pred_d -1.09 so the "
        "net over-cleans midweek (23.2 percent of SSE). z-scored numeric dow puts Wed at "
        "mid-scale, not on a week circle. is_weekend already exists. Add unused dow_sin, "
        "do not retry iws_clip100."
    ),
    "--citations",
    (
        "Vaswani, Ashish; Shazeer, Noam; Parmar, Niki; Uszkoreit, Jakob; Jones, Llion; "
        "Gomez, Aidan N.; Kaiser, Lukasz and Polosukhin, Illia 2017 NeurIPS 'Attention "
        "Is All You Need' (arXiv:1706.03762) — sinusoidal encodings map a periodic "
        "integer onto a circle so adjacent days wrap, unlike a z-scored linear dow that "
        "puts Sunday far from Monday. Relevance: Exp136 already has numeric dow and "
        "is_weekend but Wednesday still over-cleans pred_d -1.09 versus need +1.25 and "
        "owns 23.2 percent of SSE, so adding unused dow_sin is one period-7 encoding on "
        "the Exp136 recipe, not another Iws transform."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding dow_sin on the Exp136 MLP recipe (batch 16, hidden "
        "256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, "
        "pm25_accel, vent_index, Smooth-L1, Exp97 features plus sin(2 pi dow / 7)) will "
        "cut 2013 val RMSE because the mechanism is a smooth weekday circle so Wednesday "
        "is not treated as mid-scale mean-reverting persist. Per Vaswani et al. 2017 that "
        "is a sinusoidal positional encoding. Because iws_clip100 just failed, this is "
        "unused dow_sin not another Iws transform. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if linear-dow Wednesday over-clean was a 2013 tax. A val RMSE "
        "above 22.85 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
