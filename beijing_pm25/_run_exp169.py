"""Exp169 — MLP add se_pm25 on Exp167 residual recipe (MLP cycle 45/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--add-feature", "se_pm25",
    "--description", "MLP add se_pm25 on Exp167 residual recipe (MLP cycle 45/50)",
    "--diagnosis",
    (
        "1h champion is now Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck, January 31.22 versus persist-1 33.58 and JJA 13.87, hour 20 32.68 "
        "versus persist 33.24, onset n=83 RMSE 110.28 losing to persist-1 107.80. Exp168 "
        "huber_beta=20 inverted onset pred_d to -1.06. New: onset plus SE persist 50-150 "
        "n=21 RMSE 157.60 versus persist 156.55 (16.29 percent of SSE), need +115.48 "
        "pred_d +2.09 so windy southerly moderate-haze hours explode while the residual "
        "net stays at lag-1 (pred 96.8 versus actual 210.1). se_iws already failed as a "
        "wind product. Add unused se_pm25, not another huber_beta."
    ),
    "--citations",
    (
        "Guo, Song; Hu, Min; Zamora, Misti L. et al. 2014 Proceedings of the National "
        "Academy of Sciences 'Elucidating severe urban haze formation in China' "
        "(doi:10.1073/pnas.1419604111) — explosive PM2.5 growth under southerly flow is "
        "regional advection of an already-polluted North China Plain plume, so the increment "
        "scales with upwind load not with wind speed. Relevance: Exp167 onset plus SE persist "
        "50-150 still posts pred_d +2.09 versus need +115.48 at 157.60 versus persist 156.55, "
        "and se_iws already failed as a speed product, so adding unused se_pm25 equals "
        "cbwd_SE times pm25_lag1 is one pollution-payload interaction, not another Iws product."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding se_pm25 on the Exp167 residual MLP recipe (hidden "
        "512-256-128, batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, residual "
        "true, log_iws, month_sin, pm25_accel, vent_index, layer_norm off, clip=1.0, "
        "huber_beta=1) will cut 2013 val RMSE because the mechanism is an explicit "
        "southerly pollution payload so moderate-haze SE hours can leave lag-1 instead of "
        "persist-locking at pred_d +2.09 versus need +115. Per Guo et al. 2014 that is "
        "regional advection. Because huber_beta just inverted onset, this is unused "
        "PM-times-direction not another loss. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 19.6 to 22.4 versus Exp167 20.072, val 21.40 to 23.00, and "
        "composite -23.00 to -21.40. Val may move from 21.972 toward 21.50 to 21.90 if "
        "southerly payload-blind persist-lock on 2013 onsets was a val tax. A val RMSE "
        "above 22.80 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
