from __future__ import annotations

def detect_frameworks(imports: list, dependencies: list):
    keys = sorted(set((imports or []) + (dependencies or [])))
    mapping = {
      "react":"React","next":"Next.js","vue":"Vue","angular":"Angular","django":"Django","flask":"Flask",
      "fastapi":"FastAPI","express":"Express","nestjs":"NestJS","spring":"Spring","laravel":"Laravel",
      "flutter":"Flutter","react-native":"React Native"
    }
    out=[]
    for k,v in mapping.items():
        if any(k in x.lower() for x in keys):
            out.append(v)
    return sorted(set(out))
