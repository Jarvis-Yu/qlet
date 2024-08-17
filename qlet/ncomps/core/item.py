from __future__ import annotations
from collections import deque
from inspect import isfunction
from itertools import repeat
from typing import Any, Callable, Iterable, Sequence

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
            children: Item | Sequence[Item] = (),
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
            id = ""
            displayed_name = f"{self.__class__.__name__}_{_id(self)}"
        else:
            displayed_name = id
        assert id not in {_PARENT, _SELF}
        assert not id.startswith('_'), f"id cannot start with '_': {id}"
        assert not id.endswith('_'), f"id cannot end with '_': {id}"
        assert not bool(id) or id.isidentifier(), f"id is not a valid identifier: {id}"

        self.id = id
        self.displayed_id = displayed_name
        self.root = root
        self._adopt_id: str | None = None
        self.children: list[Item] = []
        self.parent: Item | None = None

        self._properties: dict[str, _ItemProperty] = {}

        self._pedigree: _Pedigree = _Pedigree(self, {}, {})
        self._pedigree_up_to_date = root

        self._set_kwargs(**kwargs)

        if not isinstance(children, Sequence):
            children = (children,)
        for child in children:
            self.add_child(child)

    @property
    def peer_id(self) -> str:
        if self._adopt_id is None:
            return self.id
        return self._adopt_id

    def _add_property(self, key: str, value: Any) -> None:
        """ adds a new property to self """
        assert len(key) > 0, f"Empty key is not allowed: \"{key}\""
        assert key[0] != '_', f"Self-defined values must not start with '_': \"{key}\""
        assert key[-1] == '_', f"Self-defined values must end with '_': \"{key}\""
        assert key not in self._properties, "_add_property() is only responsible for new properties"
        if not isfunction(value):
            self._properties[key] = _ItemProperty(key, value, lambda _: value, True)
        else:
            self._properties[key] = _ItemProperty(key, _NULL, value, False)

    def _update_property(self, key: str, value: Any) -> None:
        """ updates an existing property """
        assert key in self._properties, "_update_property() is only responsible for updating existing properties"
        property = self._properties[key]
        if not isfunction(value):
            property.set_new_value(value)
        else:
            property.set_new_f_value(value)

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

    def add_child(self, new_child: Item) -> None:
        for child in self.children:
            child._outdate_pedigree()
        self.children.append(new_child)
        new_child._set_parent(new_child)

    def _set_parent(self, parent: Item) -> None:
        assert self.parent is None, "An item can only have one parent in their life."
        self.parent = parent

    def set_parent(self, parent: Item) -> None:
        parent.add_child(self)

    def _children_dict(self) -> dict[str, Item]:
        mapping: dict[str, Item] = {}
        for child in self.children:
            if child.peer_id not in mapping:
                mapping[child.peer_id] = child
        return mapping

    def _outdate_pedigree(self) -> None:
        self._pedigree_up_to_date = False

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

    def _compute_new_requirements(self) -> None:
        """
        Updates requirements so all references follow the (potentially) new
        pedigree.
        """
        for property in self._properties.values():
            if any(
                    p is not self._pedigree._get_property((k1, k2))
                    for (k1, k2), p in property.requirements.items()
            ):
                property.compute_new_requirements(self._pedigree)
        for child in self.children:
            child._compute_new_requirements()

    def _compute_properties(self, queue: deque[tuple[Item, _ItemProperty]]) -> None:
        """ Updates queued properties according to the current definitions """
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
                p.requires_update
                for p in property.requirements.values()
            ))  # property up-to-date implies no requirement needs update
            if property.requires_update and any(
                    p.requires_update
                    for p in property.requirements.values()
            ):  # requirement needs update, computation delayed
                queue.append((item, property))
            elif property.requires_update:
                succ = property.try_update(item._pedigree)
                if not succ:
                    queue.append((item, property))

    def _compute_self_properties(self) -> None:
        """ This method assumes all requirements are up-to-date. """
        queued_properties: set[tuple[Item, _ItemProperty]] = set(zip(repeat(self), self._properties.values()))
        queue: deque[tuple[Item, _ItemProperty]] = deque(list(queued_properties))
        self._compute_properties(queue)

    def _compute_children_properties(self) -> None:
        """ This method assumes all requirements are up-to-date. """
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
        self._compute_new_requirements()
        self._compute_self_properties()
        self._compute_children_properties()


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
        self._requirements: dict[tuple[str, str], _ItemProperty] = {}
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
    def requirements(self) -> dict[tuple[str, str], _ItemProperty]:
        return self._requirements

    @property
    def dependents(self) -> set[_ItemProperty]:
        return self._dependents

    def set_new_value(self, value: Any) -> None:
        self.remove_as_dependent(self._requirements.values())
        self.remove_requirements()
        if self.up_to_date and value != self.value:
            self.notify_update()
        self._value = value
        self._f_value = lambda _: value
        self._up_to_date = True

    def set_new_f_value(self, f_value: Callable) -> None:
        self.remove_as_dependent(self._requirements.values())
        self.remove_requirements()
        was_up_to_date = self.up_to_date
        self._up_to_date = False
        self._value = _NULL
        self._f_value = f_value
        if was_up_to_date:
            self.notify_update()

    def add_dependent(self, property: _ItemProperty) -> None:
        self._dependents.add(property)

    def add_as_dependent(self, properties: Iterable[_ItemProperty]) -> None:
        for property in properties:
            property.add_dependent(self)

    def remove_dependent(self, property: _ItemProperty) -> None:
        self._dependents.remove(property)

    def remove_dependents(self) -> None:
        self._dependents.clear()

    def remove_as_dependent(self, properties: Iterable[_ItemProperty]) -> None:
        for property in properties:
            property.remove_dependent(self)

    def add_requirement(self, item_name: str, property_name: str, property: _ItemProperty) -> None:
        self._requirements[(item_name, property_name)] = property

    def remove_requirement(self, item_name: str, property_name: str) -> None:
        del self._requirements[(item_name, property_name)]

    def remove_requirements(self) -> None:
        self._requirements.clear()

    def remove_as_requirement(self, item_name: str, property_name: str) -> None:
        for dependent in self._dependents:
            dependent.remove_requirement(self)

    def compute_new_requirements(self, pedigree: _Pedigree) -> None:
        """ reset requirements according to pedigree, and notify update if necessary """
        old_props = set(self.requirements.values())
        self._requirements = {
            key: pedigree._get_property(key)
            for key in self.requirements
        }
        new_props = set(self.requirements.values())
        removed_props, added_props = old_props - new_props, new_props - old_props
        self.remove_as_dependent(removed_props)
        self.add_as_dependent(added_props)
        was_up_to_date = self.up_to_date
        self._up_to_date = False
        if was_up_to_date:
            self.notify_update()

    def notify_update(self) -> None:
        """ Notify all known dependents the value may require an update.  """
        for dependent in self._dependents:
            was_up_to_date = dependent.up_to_date
            dependent._up_to_date = False
            if was_up_to_date:
                dependent.notify_update()

    def try_update(self, pedigree: _Pedigree) -> bool:
        """
        :returns: (new value is up-to-date, new requirements)

        Update value if self is not up-to-date.
        """
        if self.up_to_date:
            return True
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
        old_reqs = set(self._requirements.keys())
        removed_reqs, added_reqs = old_reqs - requirements, requirements - old_reqs
        self.remove_as_dependent([
            self._requirements[req]
            for req in removed_reqs
        ])
        for req in removed_reqs:
            self.remove_requirement(*req)
        for req in added_reqs:
            self.add_requirement(*req, pedigree._get_property(req))
        self.add_as_dependent([
            self._requirements[req]
            for req in added_reqs
        ])
        succ = all(
            pedigree._get_property(req).up_to_date
            for req in requirements
        )
        if succ:
            self._up_to_date = True
        return succ


class _PropertyHandle:
    """
    This is a proxy providing access to accessible properties of the item.
    It can record all accesses.
    """
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
    This is a proxy providing access to accessible items in the pedigree.
    It can record all accesses.
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
