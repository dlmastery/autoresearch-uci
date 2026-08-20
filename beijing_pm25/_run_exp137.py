"""Exp137 — MLP add pm25_roll6max on Exp136 recipe (MLP cycle 13/50)."""
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
    "--add-feature", "pm25_roll6max",
    "--description", "MLP add pm25_roll6max on Exp136 recipe (MLP cycle 13/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, gap 0.092. New: hours fallen >=80 from the 6h lag peak n=620 RMSE 27.53 "
        "versus CatBoost 26.26 and persist 32.91, need -8.11 pred_d -9.03 so the net "
        "over-cleans after a crash. At-peak hours n=2685 need +3.80 pred_d +1.38 "
        "(under-build, 43.8 percent of SSE). Lags do not mark the episode peak. Add "
        "unused roll6max, do not retry vent_index."
    ),
    "--citations",
    (
        "Lim, Bryan; Arik, Sercan O.; Loeff, Nicolas and Pfister, Tomas 2021 IJCAI "
        "'Temporal Fusion Transformers for Interpretable Multi-horizon Time Series "
        "Forecasting' (arXiv:1912.09363) — local lookback statistics are first-class "
        "known inputs so a net can tell whether the latest lag is still the episode "
        "peak or already a crash from it. Relevance: Exp136 has 24 lags and delta1 but "
        "post-peak drop>=80 hours still lose CatBoost 27.53 versus 26.26 with pred_d "
        "-9.03 versus need -8.11, so adding unused max(lag1..lag6) is one episode-peak "
        "feature on the Exp136 recipe, not another vent product."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pm25_roll6max on the Exp136 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus max of lag "
        "1-6) will cut 2013 val RMSE because the mechanism is an explicit 6h episode "
        "peak so post-crash hours are not treated like never-peaked persist. Per Lim "
        "et al. 2021 that is a local lookback statistic. Because vent_index just helped "
        "2013 val and missed the 1h gate, this is unused roll6max not another mixing "
        "product. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.4 versus Exp97 20.735 and Exp136 20.509, val "
        "21.65 to 22.95, and composite -22.95 to -21.65. Val may move from 22.259 toward "
        "21.90 to 22.16 if post-peak over-clean was a 2013 tax. A val RMSE above 22.80 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
