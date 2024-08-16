from __future__ import annotations
from typing import Any

class _NullValue:
    def __getattribute__(self, name: str) -> Any:
        print("__getattribute__")
        return _NullValue

    def _NULL(self, *args, **kwargs) -> _NullValue:
        return self
    def _NULL_1(self, *args, **kwargs) -> tuple[_NullValue, _NullValue]:
        return (self, )
    def _NULL_2(self, *args, **kwargs) -> tuple[_NullValue, _NullValue]:
        return self, self

    __add__ = _NULL
    __sub__ = _NULL
    __mul__ = _NULL
    __floordiv__ = _NULL
    __truediv__ = _NULL
    __mod__ = _NULL
    __divmod__ = _NULL_2
    __radd__ = _NULL
    __rsub__ = _NULL
    __rmul__ = _NULL
    __rfloordiv__ = _NULL
    __rtruediv__ = _NULL
    __rmod__ = _NULL
    __rdivmod__ = _NULL_2
    __rpow__ = _NULL
    __and__ = _NULL
    __or__ = _NULL
    __xor__ = _NULL
    __lshift__ = _NULL
    __rshift__ = _NULL
    __rand__ = _NULL
    __ror__ = _NULL
    __rxor__ = _NULL
    __rlshift__ = _NULL
    __rrshift__ = _NULL
    __neg__ = _NULL
    __pos__ = _NULL
    __invert__ = _NULL
    __trunc__ = _NULL
    __ceil__ = _NULL
    __floor__ = _NULL
    __round__ = _NULL
    __getnewargs__ = _NULL_1
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, _NullValue)
    def __lt__(self, other: Any) -> bool:
        return not isinstance(other, _NullValue)
    __float__ = _NULL
    __int__ = _NULL
    __abs__ = _NULL
    def __hash__(self) -> int:
        return hash(self.__class__.__name__)
    def __bool__(self) -> bool:
        return False
    def __index__(self) -> int:
        0


if __name__ == "__main__":
    print(_NullValue() > _NullValue())
    print(_NullValue() == _NullValue())
    print(_NullValue() < _NullValue())
