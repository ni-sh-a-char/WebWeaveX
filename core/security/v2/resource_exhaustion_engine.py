from __future__ import annotations
def safe_resource_use(cpu_ms:int, mem_bytes:int, cpu_limit:int=30000, mem_limit:int=1_000_000_000):
    return cpu_ms<=cpu_limit and mem_bytes<=mem_limit
