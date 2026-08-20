"""Exp135 — MLP add pm25_accel on Exp134 recipe (MLP cycle 11/50)."""
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
    "--description", "MLP add pm25_accel on Exp134 recipe (MLP cycle 11/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp134 MLP val 22.432 test "
        "20.450. New: accel-q4 n=1941 (mean second-diff +26.4) is 31.5 percent of Exp134 "
        "SSE, RMSE 23.22 versus CatBoost 24.38 and persist 25.11, need +1.11 pred_d -0.02 "
        "so the net under-builds when persist is already accelerating. pm25_delta1 is in "
        "the recipe but not the change of delta. Surprise onset accel<=0 n=35 RMSE 138.71 "
        "versus persist 133.37. Add unused pm25_accel, do not retry month_sin."
    ),
    "--citations",
    (
        "Oreshkin, Boris N.; Carpov, Dmitri; Chapados, Nicolas and Bengio, Yoshua 2020 "
        "ICLR 'N-BEATS: Neural basis expansion analysis for interpretable time series "
        "forecasting' (arXiv:1905.10437) — backward residual stacks learn local "
        "polynomial trend bases, including acceleration, that a flat lag vector buries. "
        "Relevance: Exp134 already has 24 lags and pm25_delta1 but accel-q4 still "
        "under-builds pred_d -0.02 versus need +1.11 and owns 31.5 percent of SSE, so "
        "adding the unused 3-lag second difference is one local-trend feature on the "
        "Exp134 recipe, not another month or log-Iws transform."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pm25_accel on the Exp134 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, Smooth-L1, Exp97 features plus lag1-2*lag2+lag3) will cut 2013 val "
        "RMSE because the mechanism is an explicit second difference so accelerating "
        "persist hours are not treated as mean-reverting delta1. Per Oreshkin et al. "
        "2020 that is a local trend basis. Because month_sin just helped February and "
        "missed the val gate, this is unused accel not another calendar feature. KEEP "
        "if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.2 to 22.5 versus Exp97 20.735 and Exp134 20.450, val "
        "21.75 to 23.10, and composite -23.10 to -21.75. Val may move from 22.432 toward "
        "21.95 to 22.30 if accel-q4 under-build was a 2013 tax. A val RMSE above 22.90 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
