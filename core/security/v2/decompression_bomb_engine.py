from __future__ import annotations
def safe_decompression_ratio(uncompressed:int,compressed:int,max_ratio:float=100.0):
    return compressed>0 and (uncompressed/compressed)<=max_ratio
