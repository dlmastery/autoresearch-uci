# AutoResearch Process — Grok as expert air-quality nowcast researcher

## Karpathy's original principle (github.com/karpathy/autoresearch)

modify → train → check if improved → keep/discard → repeat.

## Our adaptation (verbatim from dlmastery/autoresearch, domain swapped)

Same keep/discard loop, three critical differences:

1. **NEVER deviate far from the winner.** Start every experiment from `best_config.json`.
2. **Grok IS the expert researcher.** Diagnose per-window, cite literature, form hypotheses. No blind exploration.
3. **Iteration-bound, not time-bound.** Trees stop on early stopping; nets run to patience.

## Core invariant

Always start from the current best config. Modify ONE thing. Keep if composite improves. Revert if not. Never wander off.

## The Loop (every iteration)

### Step 1: Read results
`experiment_log.jsonl`, `best_config.json`, val AND test RMSE.

### Step 2: Diagnose
- Episode vs calm residuals
- Train-test gap (overfit)
- Val-test consistency
- Composite bottleneck (`min(-val,-test)` which side)
- Trajectory (progress vs cycling)

### Step 3: Research
Ventilation / inversion / GBM nowcast / lag structure papers that match the diagnosed failure.

### Step 4: Hypothesize
Specific, falsifiable. Not "maybe more trees."

### Step 5: Design ONE experiment
One change. Justify every number.

### Step 6: Run and analyse
Compare to prediction. KEEP iff composite improved and leakage-guard passes.

### Step 7: Decide next direction
KEEP → local tweaks. 3+ REVERT on one axis → rethink diagnosis.

## Anti-patterns

| Never | Instead |
|---|---|
| Let me try X | diagnosis + paper + mechanism |
| Grid 5 learning rates | one justified value |
| Change 2+ things | sequence them |
| Ignore haze episodes | always slice residuals |
| Random CV | chronological holdout |

## State files

- `autoresearch_results/experiment_log.jsonl`
- `autoresearch_results/best_config.json`
- `autoresearch_results/dashboard.html`
- `memory/project_autoresearch_checkpoint.md`
