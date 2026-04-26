import time


class RateLimiter:
    def __init__(self, rate_per_sec):
        self.delay = 1.0 / rate_per_sec
        self.last_call = 0

    def wait(self):
        now = time.time()
        diff = now - self.last_call

        if diff < self.delay:
            time.sleep(self.delay - diff)

        self.last_call = time.time()