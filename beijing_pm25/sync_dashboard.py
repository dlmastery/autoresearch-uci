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
        "champion_diagnostics.json",
        "forensic_report.md",
        "audit_report.md",
        "autoresearch_report.md",
    ):
        p = SRC / name
        if p.exists():
            shutil.copy2(p, DST / name)
    for name in ("split_manifest.json",):
        p = DATA / name
        if p.exists():
            shutil.copy2(p, DST / name)
    extra = {
        HERE / "BACKBONE_CAMPAIGN.md": DST / "BACKBONE_CAMPAIGN.md",
        HERE / "SOTA.md": REPO / "docs" / "SOTA.md",
        REPO / "SOTA.md": REPO / "docs" / "SOTA.md",
        REPO / "WHY_THIS_BENCHMARK.md": REPO / "docs" / "WHY_THIS_BENCHMARK.md",
        REPO / "paper.md": REPO / "docs" / "paper.md",
    }
    for src, dest in extra.items():
        if src.exists() and src.resolve() != dest.resolve():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
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
