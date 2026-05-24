# Testing Log - 2026-05-24

## Scope
- Pre-trial smoke and operational tests
- Predicate invention tests
- Adversarial trial orchestration and adjudication
- Emergence stress and inferno harness creation
- GPU acceleration enablement and verification

## Environment
- OS: Windows
- Python: 3.12.10
- GPU: NVIDIA GeForce RTX 3050
- Driver: 595.79
- CUDA runtime (driver): 13.2
- Torch runtime: `2.11.0+cu128`
- Torch CUDA: `12.8`
- `torch.cuda.is_available()`: `True`

## Adversarial Trial Records

### Invalidated Run
- Run ID: `2026-05-24_135248`
- Status: `ABORTED_INVALID_ENDPOINT_MODE`
- Reason: endpoint returned echo-mode responses during adjudication path
- Evidence:
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_135248/RUN_INVALIDATION.md`
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_135248/execution_log.csv`
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_135248/execution_log.aborted_snapshot.csv`

### Valid Completed Run
- Run ID: `2026-05-24_142927`
- Preflight gate: passed
- Round 1: 5/5 PASS
- Round 2: 5/5 PASS
- Round 3: 5/5 PASS
- Total: 15/15 PASS
- Evidence:
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_142927/execution_log.csv`
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_142927/ROUND1_SUMMARY_2026-05-24.md`
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_142927/ROUND2_SUMMARY_2026-05-24.md`
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_142927/ROUND3_SUMMARY_2026-05-24.md`
  - `Adversarial_Trial_Test_Suite/runs/2026-05-24_142927/FULL_TRIAL_SUMMARY_2026-05-24.md`

## Emergence / Inferno Testing
- Added `tests/emergence_stress_1000.py` with DSAE routing + telemetry buckets.
- Added `tests/inferno_predicate_gauntlet_1000.py` with adaptive adversarial modes.
- Added invention dedupe/cap behavior in `skg-core/skg/invent_predicate.py`.
- Observed pattern in long runs:
  - alternating zero-add churn and burst edge commits
  - high structural density from scaffold/meta recursion
  - confirms generative robustness; does not alone confirm semantic utility

## Interpretation Note (Official)
Raw density in these runs is interpreted as **structural connectivity pressure**, not direct reasoning quality.  
Adjusted semantic metrics are required for quality claims.

