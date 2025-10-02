class Rect:
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int):
        self._start_x = start_x
        self._start_y = start_y
        self._end_x = end_x
        self._end_y = end_y

    def destruct(self):
        # No-op like in C#
        pass

    def get_start_x(self) -> int:
        return self._start_x

    def get_start_y(self) -> int:
        return self._start_y

    def get_end_x(self) -> int:
        return self._end_x

    def get_end_y(self) -> int:
        return self._end_y

    def is_inside(self, *args) -> bool:
        """
        Overloaded version:
        - is_inside(x, y)
        - is_inside(rect)
        """
        if len(args) == 1 and isinstance(args[0], Rect):
            rect = args[0]
            if self._start_x <= rect._start_x and self._start_y <= rect._start_y:
                return self._end_x > rect._end_x and self._end_y > rect._end_y
            return False

        elif len(args) == 2:
            x, y = args
            if self._start_x <= x and self._start_y <= y:
                return self._end_x >= x and self._end_y >= y
            return False

        else:
            raise TypeError("is_inside() expects (x, y) or (Rect)")