"""Exp31 — add Liang 2015 heating-season flag to LightGBM champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "add is_heating Nov-Feb flag to Exp30 LightGBM",
    "--add-feature", "is_heating",
    "--diagnosis",
    (
        "Champion is now Exp30 LightGBM num_leaves 63, composite -22.397, test 20.945, "
        "val 22.397. Two LightGBM KEEPs in a row improved val more than test. January "
        "on Exp29 was still RMSE 32.78 versus summer 14.07. Onset RMSE remains about 110. "
        "Hyperparameter local tweaks are shrinking val by 0.03. The original process after "
        "a KEEP that does not fix the diagnosed regime is to add a feature that names that "
        "regime. Liang 2015 winter heating is the missing binary split."
    ),
    "--citations",
    (
        "Liang, Zou, Guo, Li, Zhang, Zhang, Huang and Chen 2015 Proceedings of the Royal "
        "Society A 'Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and "
        "winter heating' — winter heating is a documented regime shift, not a smooth "
        "temperature effect, which is why a binary Nov-Feb flag is the one-thing change. "
        "Ke et al. 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision "
        "Tree' — a single extra binary column is a cheap leaf-wise split for that regime."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_heating (November through February) will cut "
        "January RMSE because the mechanism is an explicit heating-season split that "
        "temperature and dewpoint only approximate, per Liang et al. 2015. The model "
        "currently has to rediscover winter from TEMP and month harmonics. One binary "
        "feature, no other change."
    ),
    "--prediction",
    (
        "Composite predicted -22.6 to -22.1. Test RMSE 20.5 to 21.2. January RMSE should "
        "move from 32.8 toward 28 to 32. If January does not move, the flag is redundant "
        "with TEMP and this is a DISCARD."
    ),
])
