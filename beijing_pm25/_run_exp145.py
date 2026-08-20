"""Exp145 — MLP add iws_clip100 on Exp136 recipe (MLP cycle 21/50)."""
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
    "--add-feature", "iws_clip100",
    "--description", "MLP add iws_clip100 on Exp136 recipe (MLP cycle 21/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: Iws 5-20 persist>=150 "
        "n=373 RMSE 40.49 versus CatBoost 38.50 and persist 47.43 (18.3 percent of SSE). "
        "Test Iws median 4.92 std 41.64 p99 232 so Iws=10 is only +0.12 sigma after "
        "z-score and the haze-wind band collapses into calm. log_iws already logs. Add "
        "unused iws_clip100, do not retry is_janfeb."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11959) "
        "— MLP tabular models are sensitive to numerical scale, so a heavy-tailed column "
        "after z-score buries the mid-range that actually predicts the target. Relevance: "
        "Exp136 already z-scores Iws and has log_iws but Iws 5-20 persist>=150 still "
        "RMSE 40.49 versus CatBoost 38.50 and owns 18.3 percent of SSE, so adding unused "
        "min(Iws,100) is one winsorized linear scale on the Exp136 recipe, not another "
        "calendar split."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding iws_clip100 on the Exp136 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus min(Iws,100)) "
        "will cut 2013 val RMSE because the mechanism is a winsorized linear Iws scale so "
        "the 5-20 haze-wind band is not collapsed to +0.1 sigma by the storm tail. Per "
        "Gorishniy et al. 2021 that is numerical-scale sensitivity. Because is_janfeb "
        "just inverted February RMSE, this is unused iws_clip100 not another calendar "
        "split. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the Iws z-score tail was a 2013 tax. A val RMSE above 22.85 is "
        "a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
