"""Exp150 — MLP grad_clip=0 on Exp136 recipe (MLP cycle 26/50)."""
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
    "--set", "grad_clip=0",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP grad_clip=0 on Exp136 recipe (MLP cycle 26/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. hetero_loss "
        "Exp149 inverted crash pred_d -25.16 to -19.41. New: rain persist>=100 n=79 RMSE "
        "38.52 versus CatBoost 33.16 and persist 44.20, need -14.53 pred_d -8.62 so clip=1.0 "
        "batch-16 Smooth-L1 under-washes (3.5 percent of SSE). Ir>0 overall 24.06 versus "
        "CatBoost 21.51. Disable unused grad_clip, do not retry hetero_loss."
    ),
    "--citations",
    (
        "Pascanu, Razvan; Mikolov, Tomas and Bengio, Yoshua 2013 ICML 'On the difficulty "
        "of training Recurrent Neural Networks' (arXiv:1211.5063) — clipping the global "
        "gradient L2 norm when it exceeds a threshold stops exploding RNN updates, but "
        "the same cap can shrink a rare large-residual batch on a short MLP. Relevance: "
        "Exp136 uses default clip=1.0 with batch 16 and rain persist>=100 still loses "
        "CatBoost 38.52 versus 33.16 with pred_d -8.62 versus need -14.53, so setting "
        "unused grad_clip to 0 is one unclipped AdamW step on the Exp136 recipe, not "
        "another aleatoric head."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting grad_clip from 1.0 to 0 on the Exp136 MLP recipe "
        "(batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, "
        "log_iws, month_sin, pm25_accel, vent_index, Smooth-L1 with no global-norm cap) "
        "will cut 2013 val RMSE because the mechanism is unclipped rain-batch gradients "
        "so persist>=100 washout hours are not shrunk to a typical-hour step. Per "
        "Pascanu et al. 2013 that is gradient-norm clipping, inverted here because this "
        "is a 3-layer MLP not an RNN. Because hetero_loss just under-captured large "
        "residuals, this is unused clip=0 not another loss head. KEEP if 1h composite "
        "beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if clipped rain-washout batches were a 2013 tax. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
