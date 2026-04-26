import heapq


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = 0
    
    def add(self, url, priority=0):
        heapq.heappush(self.heap, (-priority, self.counter, url))
        self.counter += 1
    
    def get(self):
        if not self.heap:
            return None
        return heapq.heappop(self.heap)[2]
    
    def is_empty(self):
        return len(self.heap) == 0