"""Exp171 — MLP underpred_weight=2 on Exp167 residual recipe (MLP cycle 47/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "underpred_weight=2",
    "--description", "MLP underpred_weight=2 on Exp167 residual recipe (MLP cycle 47/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck, January 31.22 versus persist-1 33.58 and JJA 13.87, hour 20 32.68 "
        "versus persist 33.24, onset n=83 RMSE 110.28 losing to persist-1 107.80. Exp170 "
        "persist residual left January onset pred_d at -9.10. New: January onset with "
        "pred_d under 0 n=9 RMSE 168.63 versus persist 141.36 (7.99 percent of SSE; need "
        "+113.78 pred_d -32.46). Collapse NW n=71 RMSE 74.80 beats persist 102.50, but "
        "January onset NW n=6 RMSE 116.14 versus persist 100.07 with pred_d -19.26 versus "
        "need +89.50, so the 71-to-6 NW vote teaches cleanout. Raise unused "
        "underpred_weight, not another persist wrap."
    ),
    "--citations",
    (
        "Yang, Yuzhe; Zha, Kaiwen; Chen, Ying-Cong; Wang, Hao and Katabi, Dina 2021 ICML "
        "'Delving into Deep Imbalanced Regression' (arXiv:2102.09554) — frequent mid-range "
        "targets dominate the empirical risk so rare high-error tails get too little "
        "gradient, which is what happens when 71 NW collapses outvote 6 January NW onsets. "
        "Relevance: Exp167 January onset pred_d<0 n=9 still posts pred_d -32.46 versus need "
        "+113.78 at 168.63 versus persist 141.36, and Smooth-L1 beta=1 treats under-prediction "
        "of a +90 jump the same as over-prediction of a typical hour, so setting unused "
        "underpred_weight=2.0 on the Exp167 residual recipe is one asymmetric-cost probe, "
        "not another huber_beta."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting underpred_weight=2.0 on the Exp167 residual MLP recipe "
        "(hidden 512-256-128, batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, "
        "residual true, log_iws, month_sin, pm25_accel, vent_index, layer_norm off, clip=1.0, "
        "huber_beta=1) will cut 2013 val RMSE because the mechanism is a 2x Smooth-L1 cost "
        "when pred is below actual so the 71 NW-collapse hours no longer drown the 6 January "
        "NW onsets that need +90. Per Yang et al. 2021 that is imbalanced-regression "
        "reweighting. Because persist residual left the anti-jump intact, this is unused "
        "sign-asymmetric cost not another identity wrap. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 19.6 to 22.4 versus Exp167 20.072, val 21.40 to 23.00, and "
        "composite -23.00 to -21.40. Val may move from 21.972 toward 21.50 to 21.90 if the "
        "71-to-6 NW cleanout vote was a 2013 tax. A val RMSE above 22.80 is a miss. Ranges "
        "are ug/m3 on the frozen timestamps."
    ),
])
