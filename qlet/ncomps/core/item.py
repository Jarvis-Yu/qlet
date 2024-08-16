from __future__ import annotations
import heapq
from collections import defaultdict, deque
from enum import Enum, auto
from inspect import isfunction
from typing import Any, Callable, Protocol, Sequence

from typing_extensions import overload

from .null_value import _NullValue


__all__ = ["Q", "_QRefHandler"]


# built-in function alias
_id = id


_PARENT = "parent"
_SELF = "self"

_PF = "_property_f_"

_NULL = _NullValue()


class _Status(Enum):
    """ Property Status """
    NULL = auto()
    UP_TO_DATE = auto()
    REQUIRES_UPDATE = auto()

    @property
    def up_to_date(self) -> bool:
        return self is _Status.UP_TO_DATE

    @property
    def requires_update(self) -> bool:
        return self is _Status.REQUIRES_UPDATE


class Item:
    def __init__(
            self,
            id: str | None = None,
            root: bool = False,
            **kwargs
    ) -> None:
        """
        Property naming convention:
        - constants do not end with '_'
        - variables end with '_'
        """
        assert id not in {_PARENT, _SELF}
        assert not id.endswith('_'), f"id cannot end with '_': {id}"
        if id is None:
            id = f"{self.__class__.__name__}<{_id(self)}>"
        self.id = id
        self.root = root
        self._adopt_id: str | None = None
        self.children: list[Item] = []
        self.parent: Item | None = None

        self._properties: dict[str, _ItemProperty] = {}

        self._pedigree: _Pedigree = _Pedigree(self, {}, {})
        self._pedigree_up_to_date = root
        # self._qref_handler = None

        self._set_kwargs(**kwargs)

    @property
    def peer_id(self) -> str:
        if self._adopt_id is None:
            return self.id
        return self._adopt_id

    # @property
    # def pedigree(self) -> _Pedigree:
    #     if self._pedigree_status.requires_update:
    #         if self._pedigree is not None:
    #             ancestors = self._pedigree._ancestors
    #         else:
    #             ancestors = self._ancestors_dict()
    #         if self.parent is None:
    #             peers = {}
    #     assert self._pedigree is not None
    #     return self._pedigree

    def _add_property(self, key: str, value: Any) -> None:
        assert len(key) > 0, f"Empty key is not allowed: \"{key}\""
        assert key[0] != '_', f"Self-defined values must not start with '_': \"{key}\""
        assert key[-1] == '_', f"Self-defined values must end with '_': \"{key}\""
        if not isfunction(value):
            self._properties[key] = _ItemProperty(key, value, lambda _: value, True)
        else:
            self._properties[key] = _ItemProperty(key, _NULL, value, False)

    def _update_property(self, key: str, value: Any) -> None:
        assert key in self._properties
        property = self._properties[key]
        if not isfunction(value):
            property.set_new_value(self._pedigree, value)
        else:
            property.set_new_f_value(self._pedigree, value)

    def _set_kwargs(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key not in self._properties:
                self._add_property(key, value)
            else:
                self._update_property(key, value)

    def __setattr__(self, name: str, value: Any) -> None:
        is_user_defined = name[0] != '_' and name[-1] == '_'
        if not is_user_defined:
            return super().__setattr__(name, value)
        else:
            return self._set_kwargs(**{name: value})

    def __getattribute__(self, name: str) -> Any:
        is_user_defined = name[0] != '_' and name[-1] == '_'
        if not is_user_defined:
            return super().__getattribute__(name)
        assert name in self._properties
        return self._properties[name].value

    def _get_property(self, name: str) -> _ItemProperty:
        return self._properties[name]

    def add_child(self, child: Item) -> None:
        ...

    def set_parent(self, parent: Item) -> None:
        assert self.parent is None
        ...

    def update_self(self) -> None:
        ...

    def update_children(self) -> None:
        ...

    def _ancestors_dict(self) -> dict[str, Item]:
        mapping: dict[str, Item] = {}
        ancestor = self.parent
        while ancestor is not None:
            if ancestor.id not in mapping:
                mapping[ancestor.id] = ancestor
            if _PARENT not in mapping:
                mapping[_PARENT] = ancestor
        return mapping

    def _peers_dict(self) -> dict[str, Item]:
        if self.parent is None:
            return {}
        return self.parent._children_dict()

    def _children_dict(self) -> dict[str, Item]:
        mapping: dict[str, Item] = {}
        for child in self.children:
            if child.peer_id not in mapping:
                mapping[child.peer_id] = child
        return mapping

    def _update_pedigrees(self) -> None:
        """ update pedigree for all offsprings but self """
        assert self._pedigree_up_to_date
        if any(
            not child._pedigree_up_to_date
            for child in self.children
        ):
            ancestors = self._pedigree._ancestors.copy()
            ancestors[_PARENT] = self
            ancestors[self.id] = self
            peers = self._children_dict()
            for child in self.children:
                if not child._pedigree_up_to_date:
                    child._pedigree = _Pedigree(child, ancestors, peers)
                    child._pedigree_up_to_date = True
        for child in self.children:
            child._update_pedigrees()

    def _update_self_properties(self) -> None:
        """
        This method assumes all requirements are up-to-date.
        """
        queued_properties: set[_ItemProperty] = set(self._properties.values())
        queue: deque[_ItemProperty] = deque(list(queued_properties))
        while queue:
            property = queue.popleft()
            print(f">>> {property._name}")
            assert not (property.up_to_date and any(
                self._pedigree._get_property(req).requires_update
                for req in property._requirements
            ))
            if property.requires_update and any(
                    self._pedigree._get_property(req).requires_update
                    for req in property._requirements
            ):
                print("Delay")
                queue.append(property)
            elif property.requires_update:
                print("Update")
                old_reqs = property.requirements
                succ, new_reqs = property.try_update(self._pedigree)
                removed_reqs, added_reqs = old_reqs - new_reqs, new_reqs - old_reqs
                property.remove_as_dependent(self._pedigree, removed_reqs)
                property.add_as_dependent(self._pedigree, added_reqs)
                if not succ:
                    print("Return back to queue")
                    queue.append(property)
            else:
                print("Const")

    def _update_children_properties(self) -> None:
        ...

    def update(self) -> None:
        self._update_pedigrees()
        self._update_self_properties()
        self._update_children_properties()

    # def on_size_update(self, width: int, height: int) -> None:
    #     ...


class _ItemProperty:
    """
    Responsible for handling relationship of a single property.
    """
    def __init__(
            self, name: str, value: Any, f_value: Callable, up_to_date: bool,
    ) -> None:
        assert not name.startswith('_'), f"Property name cannot start with '_': {name}"
        self._name = name
        self._value = value
        self._f_value = f_value
        self._up_to_date = up_to_date
        self._requirements: set[tuple[str, str]] = set()
        self._dependents: set[_ItemProperty] = set()

    @property
    def value(self) -> Any:
        return self._value

    @property
    def requires_update(self) -> bool:
        return not self._up_to_date

    @property
    def up_to_date(self) -> bool:
        return self._up_to_date

    @property
    def requirements(self) -> set[tuple[str, str]]:
        return self._requirements

    @property
    def dependents(self) -> set[_ItemProperty]:
        return self._dependents

    def set_new_value(self, pedigree: _Pedigree, value: Any) -> None:
        self.remove_as_dependent(pedigree, self._requirements)
        self.remove_requirements()
        if self.up_to_date and value != self.value:
            self.notify_update()
        self._value = value
        self._f_value = lambda _: value
        self._up_to_date = True

    def set_new_f_value(self, pedigree: _Pedigree, f_value: Callable) -> None:
        self.remove_as_dependent(pedigree, self._requirements)
        self.remove_requirements()
        was_up_to_date = self.up_to_date
        self._up_to_date = False
        self._value = _NULL
        self._f_value = f_value
        if was_up_to_date:
            self.notify_update()

    def add_dependent(self, property: _ItemProperty) -> None:
        self._dependents.add(property)

    def add_as_dependent(self, pedigree: _Pedigree, requirements: set[tuple[str, str]]) -> None:
        for ref in requirements:
            pedigree._get_property(ref).add_dependent(self)

    def remove_dependent(self, property: _ItemProperty) -> None:
        self._dependents.remove(property)

    def remove_dependents(self) -> None:
        self._dependents.clear()

    def remove_as_dependent(self, pedigree: _Pedigree, requirements: set[tuple[str, str]]) -> None:
        for ref in requirements:
            pedigree._get_property(ref).remove_dependent(self)

    def remove_requirement(self, property: _ItemProperty) -> None:
        self._requirements.remove(property)

    def remove_requirements(self) -> None:
        self._requirements.clear()

    def remove_as_requirement(self) -> None:
        for dependent in self._dependents:
            dependent.remove_requirement(self)

    def notify_update(self) -> None:
        """
        Notify all known dependents the value may require an update.
        """
        for dependent in self._dependents:
            was_up_to_date = dependent.up_to_date
            dependent._up_to_date = False
            if was_up_to_date:
                dependent.notify_update()

    def try_update(self, pedigree: _Pedigree) -> tuple[bool, set[tuple[str, str]]]:
        """
        :returns: (new value is up-to-date, new requirements)

        Update value if self is not up-to-date.
        """
        if self.up_to_date:
            return True, self._requirements
        handle = pedigree.handle()
        try:
            handle._start_record()
            value = self._f_value(handle)
        except Exception as e:
            value = _NULL
        finally:
            handle._end_record()
            requirements = handle._requirements
        self._value = value
        self._requirements = requirements
        succ = all(
            pedigree._get_property(req).up_to_date
            for req in requirements
        )
        if succ:
            self._up_to_date = True
            print("Up-to-date now!")
        return succ, requirements


class _PropertyHandle:
    def __init__(
            self, access_name: str, item_handle: _ItemHandle, item: Item,
    ):
        self.__access_name = access_name
        self.__item_handle = item_handle
        self.__item = item

    def __getattribute__(self, name: str) -> Any:
        if name.startswith('_'):
            return super().__getattribute__(name)
        if self.__item_handle._recording:
            self.__item_handle._record((self.__access_name, name))
        return getattr(self.__item, name)


class _ItemHandle:
    def __init__(
            self, pedigree: _Pedigree,
    ) -> None:
        self.__pedigree = pedigree
        self.__recording = False
        self.__requirements: set[tuple[str, str]] = set()
        self.__property_handles: dict[str, _PropertyHandle] = {}

    @property
    def _requirements(self) -> set[tuple[str, str]]:
        return self.__requirements

    @property
    def _recording(self) -> bool:
        return self.__recording

    def _record(self, entry: tuple[str, str]) -> None:
        self.__requirements.add(entry)

    def _start_record(self) -> None:
        self.__recording = True

    def _end_record(self) -> None:
        self.__recording = False

    def __getattribute__(self, name: str) -> Any:
        if name.startswith('_'):
            return super().__getattribute__(name)
        if name not in self.__property_handles:
            item = self.__pedigree._get_item(name)
            self.__property_handles[name] = _PropertyHandle(name, self, item)
        return self.__property_handles[name]


class _Pedigree:
    """
    Identify the target item of this item given its name.
    """
    def __init__(
            self,
            this: Item,
            ancestors: dict[str, Item],
            peers: dict[str, Item],
    ) -> None:
        self._self = this
        self._ancestors = ancestors
        self._peers = peers

        self._self_alias = {_SELF, self._self.peer_id}

    def handle(self) -> _ItemHandle:
        return _ItemHandle(self)

    def _get_item(self, key: str) -> Item:
        if key in self._self_alias:
            return self._self
        if key in self._peers:
            return self._peers[key]
        return self._ancestors[key]

    def _get_property(self, keys: tuple[str, str]) -> _ItemProperty:
        item = self._get_item(keys[0])
        return item._get_property(keys[1])

    def __getitem__(self, key: str | tuple[str, str]) -> Item | _ItemProperty:
        if isinstance(key, str):
            return self._get_item(key)
        item = self._get_item(key[0])
        return item._get_property(key[1])


class _QRefUpdateQueue:
    def __init__(self) -> None:
        self.queue = []
        heapq.heapify(self.queue)

    def add(self, item) -> None:
        ...


if __name__ == "__main__":
    root = Item(
        id="root", root=True,
        v3_=lambda d: d.self.v2_ + d.self.v1_,
        v2_=lambda d: d.self.v1_ * 3,
        v1_=2,
    )
    root.update()
    print(">>> Out")
    print(root.v1_)
    print(root.v2_)
    print(root.v3_)
    print(">>> Update")
    root.v3_ = lambda d: 2 * d.self.v2_ - d.self.v1_
    root.v1_ = lambda d: d.self.v2_ / 2
    root.v2_ = 5
    root.update()
    print(">>> Out")
    print(root.v1_)
    print(root.v2_)
    print(root.v3_)
