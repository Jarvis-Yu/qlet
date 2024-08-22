from enum import Enum


__all__ = ["cached_classproperty"]


class _CachedClassProperty:
    class _Null(Enum):
        NULL = 0

    def __init__(self, fget):
        self._fget = fget
        self._cache = {}

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        if klass not in self._cache:
            self._cache[klass] = self._fget.__get__(None, klass)()
        return self._cache[klass]


def cached_classproperty(func) -> _CachedClassProperty:
    if not isinstance(func, classmethod):
        func = classmethod(func)

    return _CachedClassProperty(func)