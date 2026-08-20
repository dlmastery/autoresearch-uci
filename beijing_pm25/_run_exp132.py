"""Exp132 — MLP patience 10 to 5 on Exp130 recipe (MLP cycle 8/50)."""
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
    "--set", "patience=5",
    "--description", "MLP patience=5 on Exp130 recipe (MLP cycle 8/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp130 MLP val 22.527 test "
        "20.457 with val-test gap 2.07 versus CatBoost 1.432. Exp131 epochs=80 inverted. "
        "New: hour 13 n=333 RMSE 17.98 versus CatBoost 16.22 and persist 19.99, need "
        "-1.41 pred_d -2.30 so the net over-cleans midday. January hour 13 26.2 versus "
        "CatBoost 20.4. April hour 13 pred_d -7.1 versus need -2.0. JJA 14.15 versus "
        "13.84. Tighten unused Smooth-L1 patience, do not retry epochs."
    ),
    "--citations",
    (
        "Caruana, Rich; Lawrence, Steve and Giles, C. Lee 2000 NeurIPS 'Overfitting "
        "in Neural Nets: Backpropagation, Conjugate Gradient, and Early Stopping' — "
        "validation error can rise after the training loss is still falling, so restoring "
        "an earlier checkpoint beats waiting through extra non-improving epochs. "
        "Relevance: Exp130 early-stops on Smooth-L1 with patience 10, hour 13 over-cleans "
        "versus CatBoost 17.98 versus 16.22, and stretching epochs to 80 just failed, so "
        "cutting patience from 10 to 5 is one unused stop-criterion change on the Exp130 "
        "recipe, not another cosine budget."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting patience from 10 to 5 on the Exp130 MLP recipe "
        "(batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, "
        "epochs 50, Smooth-L1, Exp97 features) will cut 2013 val RMSE because the "
        "mechanism is earlier Smooth-L1 restore so 2010-12 midday over-clean mappings "
        "cannot sharpen after the first val plateau. Per Caruana et al. 2000 that is "
        "early stopping. Because epochs=80 just failed, this is unused patience not "
        "another cosine T_max. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.2 to 22.6 versus Exp97 20.735 and Exp130 20.457, val "
        "21.85 to 23.20, and composite -23.20 to -21.85. Val may move from 22.527 toward "
        "22.00 to 22.40 if five extra non-improving epochs were a 2013 tax. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
