"""Exp65 — add heating_night (valid-time Nov-Feb x 18-06) on Exp59 t+6 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "t+6 add heating_night Nov-Feb x 18-06 on Exp59 recipe (LGB side ladder 39/50)",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
    "--add-feature", "heating_night",
    "--set", "num_leaves=31",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp59 residuals on nocturnal heating versus "
        "daytime winter, not last fire's day-of-year alias. Exp59 test 54.419 val 57.601, "
        "gap 3.18. January 83.79 versus JJA 36.27. Hour 20 63.42. Onset n=991 RMSE 92.17. "
        "New: January evening 18-23 ALL n=174 RMSE 110.12 versus January day 10-16 RMSE 50.03. "
        "January night 00-06 onsets n=41 need +112.9 while Exp59 predicts -7.3, the wrong sign. "
        "January evening onsets n=62 need +153.0 pred +41.0. January onsets are dry (inversion "
        "mean 17, DEWP -18, 103 of 134 have inv>=10) so this is not humid secondary-aerosol haze. "
        "Heating-night onsets n=331 hold 18.7 percent of 2014 SSE. doy_sin just left January "
        "onset increment at +20.9 versus need +124.6, so the hole is clock-hour times heating, "
        "not a missing Fourier. month_sin and hour_sin are already columns; 31 leaves do not "
        "spend two sequential splits on n=62 January evening jumps."
    ),
    "--citations",
    (
        "Tang, Zhang, Zhu, Song, Muenkel, Hu, Schaefer, Liu, Zhang, Wang, Xin, Suppan and Wang "
        "2016 Atmospheric Chemistry and Physics 'Mixing layer height and its implications for "
        "air pollution over Beijing, China' (doi:10.5194/acp-16-2459-2016) — ceilometer MLH over "
        "Beijing is low in autumn and winter and collapses at night, so heating emissions after "
        "18:00 sit in a shallow layer; that is the unused valid-time heating_night flag, not "
        "another day-of-year harmonic. Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS "
        "'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' (arXiv:1706.08359) — one "
        "extra binary column is a cheap leaf-wise split that two sequential cuts on month_sin "
        "and hour_sin may never form on rare January night onsets. Relevance: Exp59 January 00-06 "
        "onsets still predict -7.3 versus needed +112.9 on the frozen 2014 t+6 timestamps."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding heating_night, a valid-time binary that is one when month is "
        "November through February and hour is 18-23 or 00-06, to the Exp59 t+6 LightGBM "
        "(num_leaves 31 plus month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW), leaving "
        "every booster knob unchanged, will cut 2013 t+6 val RMSE because the mechanism is one "
        "leaf-wise split on nocturnal mixing-layer collapse during heating that month_sin and "
        "hour_sin require two sequential cuts to form. Per Tang et al. 2016 that night-winter MLH "
        "collapse is the trap. Because doy_sin and is_heating already failed, this is a "
        "clock-times-heating interaction not another season dummy. The 1h composite will DISCARD; "
        "the side-ladder KEEP is t+6 val below 57.601. This single change starts from the current "
        "t+6 recipe on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.4 to 55.6 versus Exp59 54.42, val 56.5 to 58.4, and 1h-gate "
        "composite -61 to -53 (DISCARD). January night 00-06 onset increment may move from -7.3 "
        "toward +20 to +90. January evening 18-23 onset increment may move from +41 toward +55 "
        "to +110. A val RMSE above 58.0 is a side-ladder miss. Ranges are ug/m3 on the frozen "
        "2014 timestamps."
    ),
])
