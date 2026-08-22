"""Exp192 — FT-Transformer Pre-LN add rh_iws on Exp186 recipe (FT cycle 18/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "ft_transformer",
    "--set", "d_model=64",
    "--set", "n_heads=4",
    "--set", "n_layers=3",
    "--set", "dropout=0.1",
    "--set", "lr=0.0001",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--set", "norm_first=true",
    "--add-feature", "cbwd_prev_NW",
    "--add-feature", "rh_iws",
    "--description", "FT-Transformer Pre-LN add rh_iws on Exp186 recipe (FT cycle 18/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp186 Pre-LN +cbwd_prev_NW val 22.066 typical 7.51 "
        "versus champ 7.14. iws_clip100 closed. New: heating RH>=70 Iws<5 persist>=80 "
        "n=245 RMSE 31.59 versus persist 31.57 (7.63 percent of SSE; need +0.86 pred_d "
        "-1.09) so winter moist-calm dirty hours have zero skill, and Exp186 over-cleans "
        "with pred_d -3.65 RMSE 33.10. Unused change is add rh_iws, not another Iws clip."
    ),
    "--citations",
    (
        "Cai, Wenju; Li, Ke; Liao, Hong; Wang, Huijun and Wu, Lixin 2017 Nature Climate "
        "Change 'Weather conditions conducive to Beijing severe haze more frequent under "
        "climate change' (doi:10.1038/nclimate3249) — Beijing winter haze traps under "
        "weak surface wind plus high relative humidity, so the ratio RH over Iws names "
        "the moist-calm cell that additive rh_magnus and Iws tokens miss. Relevance: "
        "Exp167 heating RH>=70 Iws<5 persist>=80 is 31.59 versus persist 31.57 with need "
        "+0.86 but Exp186 over-cleans pred_d -3.65; adding rh_iws is one unused moist-calm "
        "token on Exp186, not another iws_clip100."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding rh_iws on the unused Exp186 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW) "
        "with Exp167 features will cut 2013 val RMSE because the mechanism is an explicit "
        "RH over Iws token so winter moist-calm dirty hours are not over-cleaned (need "
        "+0.86, Exp186 pred_d -3.65, RMSE 33.10 versus persist 31.57). Per Cai et al. "
        "2017 that is the weak-wind high-RH haze trap. Because iws_clip100 DISCARD, this "
        "is unused moist-calm ratio not another Iws clip. KEEP if 1h composite beats "
        "-21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp167 20.072 and Exp186 20.483, val "
        "21.70 to 22.40, and composite -22.40 to -21.70. Val may move from Exp186 22.066 "
        "toward 21.85 to 22.00 if the extra token stops winter moist-calm over-clean. A "
        "val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
