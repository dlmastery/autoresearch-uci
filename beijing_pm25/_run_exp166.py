"""Exp166 — MLP LayerNorm on Exp164 512-wide recipe (MLP cycle 42/50)."""
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
    "--set", "hidden=[512,256,128]",
    "--set", "layer_norm=true",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP LayerNorm on Exp164 recipe (MLP cycle 42/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp164 MLP val 22.180 test "
        "20.201, January 31.90 versus JJA 13.98, hour 20 32.40, onset 111.26, 0.013 shy of "
        "Exp97. Exp165 drop accel missed val 22.448. New: typical |pred_d|>=8 n=669 RMSE "
        "15.37 versus persist 5.90 and Exp136 13.25 (4.87 percent of SSE), mean |d| 13.51 "
        "on hours that need only 4. Keep width 512. Add unused LayerNorm."
    ),
    "--citations",
    (
        "Ba, Jimmy Lei; Kiros, Jamie Ryan and Hinton, Geoffrey E. 2016 arXiv 'Layer "
        "Normalization' (arXiv:1607.06450) — per-example hidden-unit centering bounds "
        "activation scale so a few large GELU units cannot dump a huge residual "
        "correction onto an otherwise calm row. Relevance: Exp164 already z-scores "
        "features in a 512-wide trunk, but typical |pred_d|>=8 still moves 13.51 versus "
        "need about 4 at 15.37 versus persist 5.90, so adding unused LayerNorm after each "
        "linear on the Exp164 recipe is one scale-stabilizer, not another dropout or width."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting layer_norm=true on the Exp164 MLP recipe (hidden "
        "512-256-128, batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will cut 2013 val RMSE "
        "because the mechanism is per-row hidden centering so typical hours with "
        "|need|<=10 are not hit by 13 ug over-moves from a few saturated 512-wide units. "
        "Per Ba et al. 2016 that is LayerNorm. Because drop accel just missed val and "
        "dropout 0.1 is closed, this is unused LayerNorm not another regularizer HP. KEEP "
        "if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.0 to 22.6 versus Exp97 20.735 and Exp164 20.201, val "
        "21.60 to 23.10, and composite -23.10 to -21.60. Val may move from 22.180 toward "
        "21.90 to 22.16 if typical over-move was a 2013 tax. A val RMSE above 22.90 is a "
        "miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
