from __future__ import annotations
def media_metadata(name:str, size:int=0):
    return {"name":name or "", "size":int(size)}
