"""Exp133 — MLP add log_iws on Exp130 recipe (MLP cycle 9/50)."""
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
    "--description", "MLP add log_iws on Exp130 recipe (MLP cycle 9/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp130 MLP val 22.527 test "
        "20.457. Exp132 patience=5 underfit. New: rain Ir>0 n=260 RMSE 24.80 versus "
        "CatBoost 21.51 and persist 27.27, 4.8 percent of Exp130 SSE versus 3.5 percent "
        "of Exp97. Rainy high-Iws n=87 (mean Iws 30.4) RMSE 30.77 versus CatBoost 24.06, "
        "need -11.29 pred_d -3.89 so the net under-washes windy rain. June rain n=28 "
        "need -13.93 pred_d -0.97. Ir and raw Iws are already in the recipe. Add unused "
        "log_iws, do not retry patience."
    ),
    "--citations",
    (
        "Zheng, Yu; Yi, Xiuwen; Li, Ming; Li, Ruiyuan; Shan, Zhangqing; Chang, Eric "
        "and Li, Tianrui 2015 KDD 'Forecasting Fine-Grained Air Quality Based on Big "
        "Data' — operational PM2.5 nowcasts treat wind speed and weather as interacting "
        "inputs, and heavy-tailed wind must be scaled or the learner ignores rain "
        "scavenging on the calm majority. Relevance: Exp130 already has raw Iws and Ir "
        "but rainy high-Iws hours still lose CatBoost 30.77 versus 24.06, so log1p(Iws) "
        "is one unused scale on the Exp130 recipe so the MLP can compose washout, not "
        "another patience or dropout HP."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding log_iws on the Exp130 MLP recipe (batch 16, hidden "
        "256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, Smooth-L1, Exp97 "
        "features plus log1p Iws) will cut 2013 val RMSE because the mechanism is a "
        "compressed wind scale so Ir can compose washout on rainy Iws~30 hours instead "
        "of letting the Iws tail saturate GELU. Per Zheng et al. 2015 that is wind as "
        "a nowcast input. Because patience=5 just underfit, this is unused log_iws not "
        "another training-budget HP. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.2 to 22.6 versus Exp97 20.735 and Exp130 20.457, val "
        "21.85 to 23.20, and composite -23.20 to -21.85. Val may move from 22.527 toward "
        "22.00 to 22.40 if rainy high-Iws washout was a 2013 tax. A val RMSE above 22.90 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
