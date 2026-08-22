"""Exp189 — FT-Transformer Pre-LN add is_morning on Exp186 recipe (FT cycle 15/50)."""
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
    "--add-feature", "is_morning",
    "--description", "FT-Transformer Pre-LN add is_morning on Exp186 recipe (FT cycle 15/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp186 Pre-LN +cbwd_prev_NW val 22.066 typical 7.51 "
        "versus champ 7.14. Heating_night and pres_delta closed. New: hour7 persist>=80 "
        "n=173 RMSE 21.55 versus persist 28.55 (2.51 percent of SSE; need -6.84 pred_d "
        "-3.53) so rush-hour dirty hours under-clean, and Exp186 pred_d -5.63 still misses "
        "need. Unused change is add is_morning, not another weather delta."
    ),
    "--citations",
    (
        "Guo, Song; Hu, Min; Zamora, Misti L.; Peng, Jianfei; Shang, Dongjie; Zheng, Jing; "
        "Du, Zhuofei; Wu, Zhijun; Shao, Min; Zeng, Limin; Molina, Mario J. and Zhang, Renyi "
        "2014 Science 'Elucidating severe urban haze formation in China' — they show morning "
        "rush-hour NOx and a shallow mixed layer drive Beijing PM2.5 that is not a smooth "
        "hour sinusoid, so a 7-9 block token is the unused indicator. Relevance: Exp167 "
        "hour7 persist>=80 under-cleans pred_d -3.53 versus need -6.84 at 21.55 versus "
        "persist 28.55 (Exp186 pred_d -5.63); adding is_morning is one unused hour-block "
        "token on Exp186, not another pres_delta."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_morning on the unused Exp186 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW) "
        "with Exp167 features will cut 2013 val RMSE because the mechanism is one extra "
        "7-9 token so hour-7 dirty persist can drop with lag-1 (need -6.84, Exp167 pred_d "
        "-3.53, Exp186 pred_d -5.63). Per Guo et al. 2014 that is morning haze formation. "
        "Because pres_delta already DISCARD, this is unused hour-block token not another "
        "weather delta. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp167 20.072 and Exp186 20.483, val "
        "21.70 to 22.40, and composite -22.40 to -21.70. Val may move from Exp186 22.066 "
        "toward 21.85 to 22.00 if the extra token steps hour-7 washout. A val RMSE above "
        "22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
