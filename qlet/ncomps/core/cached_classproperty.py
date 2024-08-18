from enum import Enum


__all__ = ["cached_classproperty"]


class _CachedClassProperty:
    class _Null(Enum):
        NULL = 0

    def __init__(self, fget):
        self._fget = fget
        self._cache = _CachedClassProperty._Null.NULL

    def __get__(self, obj, klass=None):
        if self._cache is not _CachedClassProperty._Null.NULL:
            return self._cache
        if klass is None:
            klass = type(obj)
        self._cache = self._fget.__get__(obj, klass)()
        return self._cache


def cached_classproperty(func) -> _CachedClassProperty:
    if not isinstance(func, classmethod):
        func = classmethod(func)

    return _CachedClassProperty(func)