"""Exp66 — t+6 reg_alpha=1 L1 leaf shrink on Exp59 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 reg_alpha=1 L1 leaf shrink on Exp59 recipe (LGB side ladder 40/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--set", "num_leaves=31",
    "--set", "reg_alpha=1",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp59 residuals on already-dirty hours that "
        "keep rising, not last fire's nocturnal-heating clock. Exp59 test 54.419 val 57.601, "
        "gap 3.18. January 83.79 versus JJA 36.27. Hour 20 63.42. Onset n=991 RMSE 92.17. "
        "New: wrong-sign onsets (need>50 but predicted increment <0) n=180 RMSE 126.85, "
        "persist 210.8, need +90.9, pred -24.4, 12.3 percent of SSE. Daytime onsets with "
        "persist>=150 n=79 need +88.5 pred -22.7, so the sign error is not a night flag. "
        "Dirty-calm persist>=100 and Iws<5 is n=1842 RMSE 78.34 and 48 percent of SSE, but "
        "the cell mean is already calibrated (need -21.6, pred -18.9). Inside that cell "
        "delta1 correlates only +0.06 with the 6h change; heating_night left January night "
        "onset increment at -7.1. L2 leaves are averaging an unidentifiable onset/collapse "
        "coin-flip from 2010-2012, which is a leaf-score problem not another dummy."
    ),
    "--citations",
    (
        "Chen, Tianqi and Guestrin, Carlos 2016 KDD 'XGBoost: A Scalable Tree Boosting System' "
        "(arXiv:1603.02754) — section 2.2 puts an L1 penalty (reg_alpha) on leaf weights so "
        "rare high-loss partitions cannot keep an unshrunk value; that is the unused knob on "
        "Exp59 after L2 reg_lambda=1 already missed. Ke, Meng, Finley, Wang, Chen, Ma, Ye and "
        "Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' "
        "(arXiv:1706.08359) — LightGBM exposes the same L1 term as reg_alpha on leaf-wise "
        "scores. Relevance: Exp59 dirty-calm hours are mean-calibrated yet 180 already-dirty "
        "onsets still predict -24 versus needed +91, which is L2 leaf memorization of 2010-2012 "
        "episode tails on the frozen 2014 t+6 timestamps, not a missing calendar column."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting reg_alpha from 0 to 1 on the Exp59 t+6 LightGBM "
        "(num_leaves 31 plus month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW), "
        "leaving features unchanged, will cut 2013 t+6 val RMSE because the mechanism is L1 "
        "shrinkage of dirty-calm leaf scores that currently memorize 2010-2012 onset-versus-collapse "
        "noise. Per Chen and Guestrin 2016 that is the L1 leaf penalty. Because heating_night "
        "and doy_sin already failed and reg_lambda=1 was L2, this is L1 not another dummy or "
        "another L2. The 1h composite will DISCARD; the side-ladder KEEP is t+6 val below 57.601. "
        "This single change starts from the current t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.8 to 55.8 versus Exp59 54.42, val 56.6 to 58.4, and 1h-gate "
        "composite -61 to -53 (DISCARD). Wrong-sign onset increment may move from -24.4 toward "
        "-15 to +5. A val RMSE above 58.0 is a side-ladder miss. Ranges are ug/m3 on the frozen "
        "2014 timestamps."
    ),
])
