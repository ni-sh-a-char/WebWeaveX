# FINAL PACKAGE DISTRIBUTED EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 27 |
| PASS | 17 |
| FAIL | 10 |
| UNTESTED | 0 |
| Hash mismatches | 2 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/distributed/__init__.py` — barrel_export_mismatch:['build_frontier', 'schedule_distributed_execution', 'balance_semantic_workloads', 'create_distributed_checkpoint', 'recover_distributed_runtime']
- `core/distributed/crawl_diff_engine.py` — py=None js=(sb - sa) is not iterable
- `core/distributed/crawl_diff_v2_engine.py` — py=None js=(c - p) is not iterable
- `core/distributed/crawl_priority_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\distributed\crawlPriorityEngine.ts:10:9: ERROR: Expected ")" but found ":"
- `core/distributed/crawl_resume_engine.py` — py=JSONDecodeError: Expecting value: line 1 column 1 (char 0) js=Unexpected token 'p', "probe" is not valid JSON
- `core/distributed/distributed_checkpoint_engine.py` — py=None js=serialized.encode is not a function
- `core/distributed/distributed_recovery_engine.py` — output_or_state_mismatch
- `core/distributed/distributed_work_stealing_engine.py` — py=AttributeError: 'list' object has no attribute 'keys' js=Cannot convert undefined or null to object
- `core/distributed/freshness_v2_engine.py` — py=None js=u is not defined
- `core/distributed/shard_balancer_engine.py` — output_or_state_mismatch

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
