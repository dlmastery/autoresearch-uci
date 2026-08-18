"""Copy live results into docs/dashboard for GitHub Pages."""
from __future__ import annotations

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent if (HERE.parent / "docs").is_dir() else HERE
SRC = HERE / "autoresearch_results"
DST = REPO / "docs" / "dashboard"
DATA = HERE / "data"


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    dash = HERE / "dashboard.html"
    if dash.exists():
        shutil.copy2(dash, DST / "index.html")
        shutil.copy2(dash, SRC / "dashboard.html")
    for name in (
        "experiment_log.jsonl",
        "reasoning_annotations.json",
        "best_config.json",
        "experiment_summary.md",
        "research_journal.md",
        "persistence_baseline.json",
    ):
        p = SRC / name
        if p.exists():
            shutil.copy2(p, DST / name)
    for name in ("split_manifest.json",):
        p = DATA / name
        if p.exists():
            shutil.copy2(p, DST / name)
    trades = DST / "trade_logs"
    trades.mkdir(exist_ok=True)
    src_trades = SRC / "trade_logs"
    if src_trades.exists():
        for f in src_trades.glob("*"):
            if f.is_file() and f.suffix in {".json", ".csv"}:
                shutil.copy2(f, trades / f.name)
    print(f"synced {SRC} -> {DST}")


if __name__ == "__main__":
    main()
