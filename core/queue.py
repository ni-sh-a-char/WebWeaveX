class URLQueue:
    def __init__(self):
        self.queue = []
        self.visited = set()

    def add(self, url):
        if url not in self.visited:
            self.queue.append(url)
            self.visited.add(url)

    def get(self):
        if self.queue:
            return self.queue.pop(0)
        return None