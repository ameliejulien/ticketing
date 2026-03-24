from datetime import datetime

from src.ports.clock import Clock


class FixedClock(Clock):
    def __init__(self, fixed_time: datetime):
        self.fixed_time = fixed_time

    def now(self) -> datetime:
        return self.fixed_time
