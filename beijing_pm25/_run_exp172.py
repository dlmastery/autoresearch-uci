"""Exp172 — MLP add nw_rh on Exp167 residual recipe (MLP cycle 48/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--add-feature", "nw_rh",
    "--description", "MLP add nw_rh on Exp167 residual recipe (MLP cycle 48/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck, January 31.22 versus persist-1 33.58 and JJA 13.87, hour 20 32.68 "
        "versus persist 33.24, onset n=83 RMSE 110.28 losing to persist-1 107.80. Exp171 "
        "underpred_weight flipped January onset pred_d but taxed typical with a +4.34 ug "
        "bias. New: onset NW with RH under 30 n=5 RMSE 120.73 versus persist 103.16 "
        "(2.28 percent of SSE; need +90.80 pred_d -21.11) and January NW RH<30 persist>=80 "
        "n=26 RMSE 59.05 with pred_d -33.45 versus need -17.92 so dry NW is over-cleaned. "
        "Collapse NW RH<30 already beats persist 114.25 at 70.77. Add unused nw_rh, not "
        "another global under-pred weight."
    ),
    "--citations",
    (
        "Wang, Gehui; Zhang, Renyi; Gomez, Mario E. et al. 2016 Proceedings of the "
        "National Academy of Sciences 'Persistent sulfate formation from London Fog to "
        "Chinese haze' (doi:10.1073/pnas.1616540113) — urban haze chemistry needs high "
        "aerosol water so humid northwesterlies and dry dusty northwesterlies are not the "
        "same cleanout template. Relevance: Exp167 onset NW RH<30 still posts pred_d "
        "-21.11 versus need +90.80 at 120.73 versus persist 103.16 while collapse NW "
        "RH>=50 only under-cleans at pred_d -22.83 versus need -90.71, so adding unused "
        "nw_rh equals cbwd_NW times rh_magnus is one humidity-conditioned NW path, not "
        "another Iws product or underpred_weight."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding nw_rh on the Exp167 residual MLP recipe (hidden "
        "512-256-128, batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, residual "
        "true, log_iws, month_sin, pm25_accel, vent_index, layer_norm off, clip=1.0, "
        "huber_beta=1) will cut 2013 val RMSE because the mechanism is an explicit NW "
        "times humidity so dry January NW hours stop borrowing the moist-NW cleanout "
        "units that currently subtract 21 ug when the jump needs +91. Per Wang et al. "
        "2016 that is aerosol-water regime split. Because underpred_weight just biased "
        "every hour high, this is unused humidity-conditioned NW not another loss. KEEP "
        "if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 19.6 to 22.4 versus Exp167 20.072, val 21.40 to 23.00, and "
        "composite -23.00 to -21.40. Val may move from 21.972 toward 21.50 to 21.90 if "
        "dry-NW over-clean on 2013 heating hours was a val tax. A val RMSE above 22.80 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
