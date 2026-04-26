import threading


class MemoryContext:
    def __init__(self):
        self._lock = threading.RLock()
        self._data = {}
    
    def __contains__(self, key):
        with self._lock:
            return key in self._data
    
    def __getitem__(self, key):
        with self._lock:
            if key in self._data:
                return self._data[key]
            raise KeyError(key)
    
    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value
    
    def __len__(self):
        with self._lock:
            return len(self._data)
    
    def keys(self):
        with self._lock:
            return list(self._data.keys())
    
    def values(self):
        with self._lock:
            return list(self._data.values())
    
    def items(self):
        with self._lock:
            return list(self._data.items())
    
    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)

    def set(self, key, value):
        with self._lock:
            self._data[key] = value
    
    def setdefault(self, key, default):
        with self._lock:
            return self._data.setdefault(key, default)

    def append(self, key, value):
        with self._lock:
            self._data.setdefault(key, []).append(value)

    def get_all(self):
        with self._lock:
            return dict(self._data)
