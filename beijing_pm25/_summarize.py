import json
from pathlib import Path

p = Path(__file__).resolve().parent / "autoresearch_results" / "experiment_log.jsonl"
rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
champ = max(rows, key=lambda r: r["composite"])
print(f"n={len(rows)} keeps={sum(r['status']=='KEEP' for r in rows)}")
print(f"champion exp{champ['experiment_num']} composite={champ['composite']:.4f} test={champ['test_primary']:.4f} val={champ['val_primary']:.4f}")
print("--- KEEP lineage ---")
for r in rows:
    if r["status"] != "KEEP":
        continue
    desc = r["description"]
    print(f"{r['experiment_num']:2d} {r['backbone']:8s} test={r['test_primary']:.3f} val={r['val_primary']:.3f} c={r['composite']:.3f} {desc}")
print("--- all ---")
for r in rows:
    desc = r["description"].replace("Exp1 baseline XGBoost nowcast, Chen-Guestrin 2016 defaults, frozen calendar split train2010-12/val2013/test2014", "baseline")
    if "from champion:" in desc:
        desc = desc.split("from champion:", 1)[1].strip()
    print(f"{r['experiment_num']:2d} {r['status']:7s} {r['backbone']:8s} test={r['test_primary']:.3f} val={r['val_primary']:.3f} {desc}")
