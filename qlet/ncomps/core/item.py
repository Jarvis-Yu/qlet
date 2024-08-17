from __future__ import annotations
import heapq
from collections import defaultdict, deque
from enum import Enum, auto
from inspect import isfunction
from itertools import repeat
from typing import Any, Callable, Protocol, Sequence

from typing_extensions import overload

from .null_value import _NullValue


# built-in function alias
_id = id


_PARENT = "parent"
_SELF = "self"

_NULL = _NullValue()


class CircleException(Exception):
    """ An exception that represents infinite loop. """
    pass


class Item:
    def __init__(
            self,
            id: str | None = None,
            root: bool = False,
            children: Sequence[Item] = (),
            **kwargs
    ) -> None:
        """
        :param id: identifier of this item, cannot be ``parent`` or ``self``
        :param root: if this item is the root of the item tree for its entire life
        :param children: children items

        Property naming convention:
        - constants do not end with '_'
        - variables end with '_'
        """
        if id is None:
            class_name = self.__class__.__name__
            while class_name.startswith('_'):
                class_name = class_name[1:]
            id = f"{self.__class__.__name__}_{_id(self)}"
        assert id not in {_PARENT, _SELF}
        assert not id.startswith('_'), f"id cannot start with '_': {id}"
        assert not id.endswith('_'), f"id cannot end with '_': {id}"
        assert id.isidentifier(), f"id is not a valid identifier: {id}"

        self.id = id
        self.root = root
        self._adopt_id: str | None = None
        self.children: list[Item] = []
        self.parent: Item | None = None

        self._properties: dict[str, _ItemProperty] = {}

        self._pedigree: _Pedigree = _Pedigree(self, {}, {})
        self._pedigree_up_to_date = root

        self._set_kwargs(**kwargs)

        for child in children:
            self.add_child(child)

    @property
    def peer_id(self) -> str:
        if self._adopt_id is None:
            return self.id
        return self._adopt_id

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

    def _set_key_val(self, key: str, value: Any) -> None:
            if key not in self._properties:
                self._add_property(key, value)
            else:
                self._update_property(key, value)

    def _set_kwargs(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._set_key_val(key, value)

    def __setattr__(self, name: str, value: Any) -> None:
        is_user_defined = (not name.startswith('_')) and name.endswith('_')
        if not is_user_defined:
            return super().__setattr__(name, value)
        else:
            return self._set_key_val(name, value)

    def __getattribute__(self, name: str) -> Any:
        is_user_defined = (not name.startswith('_')) and name.endswith('_')
        if not is_user_defined:
            return super().__getattribute__(name)
        assert name in self._properties
        return self._properties[name].value

    def _get_property(self, name: str) -> _ItemProperty:
        return self._properties[name]

    def add_child(self, child: Item) -> None:
        self.children.append(child)
        child._set_parent(child)

    def _set_parent(self, parent: Item) -> None:
        assert self.parent is None, "An item can only have one parent in their life."
        self.parent = parent

    def set_parent(self, parent: Item) -> None:
        parent.add_child(self)

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

    def _compute_pedigrees(self) -> None:
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
            child._compute_pedigrees()

    def _compute_properties(self, queue: deque[tuple[Item, _ItemProperty]]) -> None:
        last_queue_len = len(queue)
        loop_count = last_queue_len + 1
        while queue:
            loop_count -= 1
            if loop_count == 0:
                if last_queue_len == len(queue):
                    raise CircleException("Dependency circle detected")
                last_queue_len = len(queue)
                loop_count = last_queue_len + 1
            item, property = queue.popleft()
            assert not (property.up_to_date and any(
                item._pedigree._get_property(req).requires_update
                for req in property._requirements
            ))  # property up-to-date implies no requirement needs update
            if property.requires_update and any(
                    item._pedigree._get_property(req).requires_update
                    for req in property._requirements
            ):  # requirement needs update, computation delayed
                queue.append((item, property))
            elif property.requires_update:
                old_reqs = property.requirements
                succ, new_reqs = property.try_update(item._pedigree)
                removed_reqs, added_reqs = old_reqs - new_reqs, new_reqs - old_reqs
                property.remove_as_dependent(item._pedigree, removed_reqs)
                property.add_as_dependent(item._pedigree, added_reqs)
                if not succ:
                    queue.append((item, property))

    def _compute_self_properties(self) -> None:
        """
        This method assumes all requirements are up-to-date.
        """
        queued_properties: set[tuple[Item, _ItemProperty]] = set(zip(repeat(self), self._properties.values()))
        queue: deque[tuple[Item, _ItemProperty]] = deque(list(queued_properties))
        self._compute_properties(queue)

    def _compute_children_properties(self) -> None:
        queued_properties: set[tuple[Item, _ItemProperty]] = set()
        for child in self.children:
            for property in child._properties.values():
                queued_properties.add((child, property))
        queue: deque[tuple[Item, _ItemProperty]] = deque(list(queued_properties))
        self._compute_properties(queue)
        for child in self.children:
            child._compute_children_properties()

    def compute(self) -> None:
        self._compute_pedigrees()
        self._compute_self_properties()
        self._compute_children_properties()

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
    """
    This is a proxy providing access to accessible properties of this or other
    items.
    """
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

    def _get_property_handle(self, name: str) -> _PropertyHandle:
        if name not in self.__property_handles:
            item = self.__pedigree._get_item(name)
            self.__property_handles[name] = _PropertyHandle(name, self, item)
        return self.__property_handles[name]

    def __getattribute__(self, name: str) -> Any:
        if name.startswith('_'):  # private attributes
            return super().__getattribute__(name)
        if name.endswith('_'):  # direct self property
            property_handle = self._get_property_handle(_SELF)
            return property_handle.__getattribute__(name)
        return self._get_property_handle(name)


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


if __name__ == "__main__":
    item1 = Item(
        id="item1",
        v1_=lambda d: d.parent.v1_ + 1,
        v2_=lambda d: d.self.v1_ + d.item2.v1_,
    )
    item2 = Item(
        id="item2",
        v1_=lambda d: d.item1.v1_ + 1,
        v2_=lambda d: d.parent.v3_ + d.item1.v2_,
    )
    root = Item(
        id="root", root=True,
        v3_=lambda d: d.self.v2_ + d.self.v1_,
        v2_=lambda d: d.self.v1_ * 3,
        v1_=2,
        children=(
            item1,
            item2,
        ),
    )
    root.compute()
    print("\n##### Update #####")
    root.v3_ = lambda d: 2 * d.self.v2_ - d.self.v1_
    root.v1_ = lambda d: d.self.v2_ / 2
    root.v2_ = 5
    item2.v2_ = lambda d: d.parent.v1_ * d.item1.v1_
    root.compute()
