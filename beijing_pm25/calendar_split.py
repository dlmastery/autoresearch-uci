"""Industry calendar-year split for UCI 381 Beijing PM2.5.

Frozen protocol (operational AQ / EPA-style future-year holdout):
  train  2010-01-01 <= t < 2013-01-01 minus 24 h embargo
  val    2013-01-01 <= t < 2014-01-01 minus 24 h embargo
  test   2014-01-01 <= t <= 2014-12-31

The 24 h embargo at each year boundary is at least the longest lag (24) and
covers a t+24 label horizon, so this split stays valid if the target later
moves from nowcast-t to forecast-t+h, h<=24.

Test timestamps are hashed. Changing them is reward hacking.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
PURGE_HOURS = 24
TRAIN_END = pd.Timestamp("2013-01-01") - pd.Timedelta(hours=PURGE_HOURS)
VAL_START = pd.Timestamp("2013-01-01")
VAL_END = pd.Timestamp("2014-01-01") - pd.Timedelta(hours=PURGE_HOURS)
TEST_START = pd.Timestamp("2014-01-01")
TEST_END = pd.Timestamp("2015-01-01")
PROTOCOL_ID = "uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h"


def _index_hash(times: pd.Series) -> str:
    payload = ",".join(pd.to_datetime(times).dt.strftime("%Y-%m-%dT%H:%M:%S"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_manifest(times: pd.Series, out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or DATA
    t = pd.to_datetime(times).reset_index(drop=True)
    n = len(t)

    train_mask = (t >= pd.Timestamp("2010-01-01")) & (t < TRAIN_END)
    val_mask = (t >= VAL_START) & (t < VAL_END)
    test_mask = (t >= TEST_START) & (t < TEST_END)
    assigned = train_mask | val_mask | test_mask

    train_idx = np.flatnonzero(train_mask.to_numpy())
    val_idx = np.flatnonzero(val_mask.to_numpy())
    test_idx = np.flatnonzero(test_mask.to_numpy())
    unused_idx = np.flatnonzero((~assigned).to_numpy())

    if len(train_idx) == 0 or len(val_idx) == 0 or len(test_idx) == 0:
        raise RuntimeError("calendar split produced an empty fold")
    if train_idx.max() >= val_idx.min() or val_idx.max() >= test_idx.min():
        raise RuntimeError("calendar split is not strictly ordered train < val < test")

    test_hash = _index_hash(t.iloc[test_idx])
    val_hash = _index_hash(t.iloc[val_idx])
    train_hash = _index_hash(t.iloc[train_idx])

    np.savez(
        out_dir / "split_indices.npz",
        train_idx=train_idx.astype(np.int64),
        val_idx=val_idx.astype(np.int64),
        test_idx=test_idx.astype(np.int64),
        unused_idx=unused_idx.astype(np.int64),
    )

    manifest = {
        "protocol_id": PROTOCOL_ID,
        "dataset": "UCI 381 Beijing PM2.5",
        "rationale": (
            "Operational air-quality practice: train on past calendar years, "
            "validate on the next full year, test on the following full year. "
            "24 h embargo at each boundary equals max lag and t+24 horizon."
        ),
        "purge_hours": PURGE_HOURS,
        "n_rows": int(n),
        "n_train": int(len(train_idx)),
        "n_val": int(len(val_idx)),
        "n_test": int(len(test_idx)),
        "n_unused_embargo": int(len(unused_idx)),
        "train_time_range": [str(t.iloc[train_idx[0]]), str(t.iloc[train_idx[-1]])],
        "val_time_range": [str(t.iloc[val_idx[0]]), str(t.iloc[val_idx[-1]])],
        "test_time_range": [str(t.iloc[test_idx[0]]), str(t.iloc[test_idx[-1]])],
        "train_hash": train_hash,
        "val_hash": val_hash,
        "test_hash": test_hash,
        "frozen": True,
        "written_at": datetime.now().isoformat(timespec="seconds"),
    }
    (out_dir / "split_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(
        f"calendar split {PROTOCOL_ID}\n"
        f"  train {manifest['n_train']:5d}  {manifest['train_time_range']}\n"
        f"  val   {manifest['n_val']:5d}  {manifest['val_time_range']}\n"
        f"  test  {manifest['n_test']:5d}  {manifest['test_time_range']}\n"
        f"  unused embargo rows {manifest['n_unused_embargo']}\n"
        f"  test_hash {test_hash}"
    )
    return manifest


def load_indices(out_dir: Path | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    out_dir = out_dir or DATA
    blob = np.load(out_dir / "split_indices.npz")
    return blob["train_idx"], blob["val_idx"], blob["test_idx"]


def register_with_framework() -> None:
    """Patch the cloned runner's split registry. Call before run_experiment()."""
    from generalized_ml_autoresearch.core.evaluation.splits import (  # type: ignore
        FoldAssignment,
        SPLIT_REGISTRY,
        _BaseSplitter,
    )

    class CalendarYearSplit(_BaseSplitter):
        def __init__(self, manifest_dir: str | None = None, **_ignored: Any):
            self.manifest_dir = Path(manifest_dir) if manifest_dir else DATA

        def split(self, n_samples: int, y=None, groups=None):
            train_idx, val_idx, test_idx = load_indices(self.manifest_dir)
            if max(train_idx.max(), val_idx.max(), test_idx.max()) >= n_samples:
                raise AssertionError(
                    f"frozen split indices exceed n_samples={n_samples}; rebuild features+split"
                )
            man = json.loads((self.manifest_dir / "split_manifest.json").read_text(encoding="utf-8"))
            if not man.get("frozen"):
                raise AssertionError("split manifest is not frozen")
            return [
                FoldAssignment(
                    0,
                    train_idx,
                    val_idx,
                    test_idx,
                    "calendar_2014_test",
                )
            ]

    SPLIT_REGISTRY["calendar_year"] = CalendarYearSplit
