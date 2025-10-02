class GameTime:
    _tick = 0

    __init__(self):
        self._tick: int = 0

    def get_tick(self) -> int: return self._tick

    def reset(self) -> None: self._tick = 0

    def increase_tick(amount: int = 1) -> None: self._tick += amount